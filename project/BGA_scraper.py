""" BGA_Scraper collects the stats of the top players of each
game from https://boardgamearena.com, for each game they have played,
including basic information about each game itself.
Basic Functionality is inherited from bot.py, and data cleaning
is carried out by cleaning.py, data is stored in the cloud by
cloud.py. More info in README.txt.

Main functionality:
------------------
log_in -- Use Scraper functions to log in, get url, send keys,
          click button
gather_game_data -- Follow link to games page, gather game data,
                    send to cleaning,
                    click extend to see more players, save the
                    link to the players stats
get_images -- Get an image from each link in the list, Saves each
              to file.
retreive_player_stats -- Follow each link to the player stats, store
                        raw stat tables using BeautifulSoup
run_scraper -- Define variables, and call functions from across the
               package to execute
                data collection, cleaning, and save data to file.
get_games_links -- visit BGA list of all games, gather links to each
                   game page, store in list

Outputs:
--------
games_data.json
games_links.json
all_top_players.json
raw_player_stats.json
cleaned_player_stats.json <- results stored here
"""

# %% Run block
import os
from bot import Scraper
import cleaning
import time
import json
from selenium import webdriver  # type: ignore
from datetime import datetime
from cloud import CloudIntegration
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


class BGAscraper(Scraper):
    def __init__(self) -> None:
        super().__init__()
        chrome_options = Options()
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.games_list = []
        self.link_list = []
        self.games_pages = []
        self.game_data = {}
        self.all_top_players = {}
        self.all_game_stats = {}
        self.raw_players_stats = {}

    def get_games_links(self) -> list:
        """ Visit the url containing all games on BGA
        and find the url for each game page.
        Remove cooperative games as these have no league tables.
        This method is outdated since the BGA website updated, 
        the next method "get_games_links_workaround" is functional.

        Returns:
        ---------
        link_list
        """

        url = 'https://boardgamearena.com/gamelist?section=all'
        soup = self.soup_page(url)

        # define variables for soup_links_from_table
        table_name = 'div'
        table_attrs = 'gamelist_itemrow_all'
        element_tag = 'a'
        link_tag = 'href'
        limit = 3    # <----------------- Limit defined here <---------------

        self.link_list = \
            self.soup_links_from_table(soup, table_name, table_attrs,
                                       element_tag, link_tag, limit)

        # these games are cooperative, and have no rankings
        coop_list = ['/gamepanel?game=thecrewdeepsea',
                     '/gamepanel?game=pandemic',
                     '/gamepanel?game=thecrew',
                     '/gamepanel?game=bandido', '/gamepanel?game=similo',
                     '/gamepanel?game=concept', '/gamepanel?game=tranquility',
                     '/gamepanel?game=forbiddenisland',
                     '/gamepanel?game=pingimus',
                     '/gamepanel?game=solarstorm', '/gamepanel?game=yokai',
                     '/gamepanel?game=hanabi', '/gamepanel?game=minhwatu',
                     '/gamepanel?game=narabi', '/gamepanel?game=hardback',
                     '/gamepanel?game=chess',
                     '/gamepanel?game=letter tycoon',
                     '/gamepanel?game=crimezoom',
                     ]
        self.remove_count = 0
        for link in self.link_list:
            for game in coop_list:
                if link == game:
                    self.link_list.remove(link)
                    self.remove_count += 1
                    break
        print('Removed coop games = ', self.remove_count)
        print(self.link_list)
        # remove cooperative games
        return self.link_list, self.remove_count

    def get_games_links_workaround(self) -> list:

        """ BGA updated their main games page, it is now
        significantly more complicated to gather a list
        of all the games, for now, this code uses the list
        of games previously gathered, contained in the
        data folder"""

        with open('./Data/full_games_links.json', mode='r') as f:
            full_link_list = json.load(f)
            limit = 2    # <----------------- Limit defined here <------------
            self.link_list = full_link_list[0:limit]

        print(f'Using stored games list with {limit} links')
        return self.link_list

    def log_in(self, url: str):
        """
        Use functions from Scraper class to log in to BGA
        with Selenium and Chrome, using my account details
        """
        # print("1", os.environ.get('BGAU'))
        # print("2", os.environ['BGAU'])

        time.sleep(4)
        self.sel_get_url(url)
        self.sel_send_keys_id(element_id=('username_input'),
                              keys=("ed.cliffe1@gmail.com"))
        self.sel_send_keys_id(element_id=('password_input'),
                              keys=("testpassword123"))
        self.sel_click_id(id=('submit_login_button'))

    def gather_game_data(self, link_list: list,
                         game_data: dict) -> dict:
        """
        Visit each page in the link_list to gather different
        game_data using Selenium, and store links to the pages
        of top players for each game

        Keyword Arguments
        -----------------
        driver - selenium webdriver
        link_list - a list of (half) the urls for each of the games.
                    link construction takes places below
        game_data - empty dictionary to store the games info.

        Returns:
        --------
        game_data - dict: game_data[game_name] = [players, playtime_cleaned,
                                                 complexity, picture_link, url]

        """
        link_list = self.link_list
        time.sleep(2)
        driver = self.driver

        # access games link list, follow each link, gather useful elements
        for link in link_list:

            url = 'https://boardgamearena.com' + link
            self.sel_get_url(url)
            time.sleep(2)

            game_name_ele = driver.find_element(By.ID, "game_name")
            game_details_ele = driver.find_element(By.CLASS_NAME, "col-md-6")

            game_picture = driver.find_element(By.CLASS_NAME, 'game_image')
            picture_link = game_picture.get_attribute('src')
            game_name = game_name_ele.text.lower()

            # clean details and add to dictionary
            game_data[game_name] = \
                cleaning.clean_games_stats(game_details_ele, picture_link, url)

            # click extend, to see more players
            xpath = '//*[@id="seemore"]'
            try:
                self.sel_click_xpath(xpath)
            except:
                print('extend not clicked', game_name)
            time.sleep(2)

            # find player table
            top_players = driver.find_element(By.CLASS_NAME, 'gameranking')

            # get each player from table, into list
            top_player_list = \
                top_players.find_elements(By.CLASS_NAME, 'playername')

            temp_players_list = []
            # get each link from player,
            # add the suffix to go to player stats page
            for item in top_player_list:
                # link = item.find_element_by_tag_name('a')
                temp_players_list.append(item.get_attribute('href')
                                         + "&section=prestige")

            # store in dictionary
            temp_players_list.pop(0)
            self.all_top_players[game_name] = temp_players_list

        return self.all_top_players, self.game_data

    def get_images(self, game_data: dict):
        """For each image link in the game_data,
        call the Scraper download_image function.
        Scraper class stores images in ./Data/Images
        """

        print('Download images')
        for k in game_data.keys():

            filename = k + '.jpg'
            url = game_data[k][3]
            self.download_image(url, filename)

        return

    def retrieve_player_stats(self, game_data: dict, all_top_players: dict):
        """For each game, visit the each of the top players
        stats page (prestige) and save the data for all their played games.
        Store in dictionary containing all gathered player stats,
        ready for cleaning.
        Log in by passing cookies and headers.

        Returns:
        --------
        Raw_player_stats format: game_name[player_name] = [stats: string] """

        print('Get player stats:')

        cookies = {
            '_ga': 'GA1.2.1178257335.1638525794',
            '__stripe_mid': '0bcc75c0-77de-41c1-bb11-2e1f1febc730b9ed6d',
            'TournoiEnLigneid': 'ieEHLqZ1UdbZy7G',
            'TournoiEnLignetk': 'XxHh33JxmRfkxFbNvhGvkliHnJ0It42Y9t37EzduApdqzUf2nETNZDvxdpRWUjST',
            '_gid': 'GA1.2.1576007387.1644267125',
            'PHPSESSID': '3aqddk6lribas15nf995u8bsoe',
            'TournoiEnLigne_sso_user': 'Edcentric%243%24ed.cliffe1%40gmail.com',
            'TournoiEnLigne_sso_id': '2fcd5e41afc058d14db982b20257edb3',
            'TournoiEnLigneidt': 'i69jwviLyoGO06B',
            'TournoiEnLignetkt': '4pzUBpMbqkH9e44jAbf0VIgcB0oz5T2q0u4MerGpKsxBDyeg8kErcdE4tc29ZHVX',
            '_gat': '1',
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'TE': 'trailers',
        }

        for name in game_data.keys():
            print(name)
            temp_stats_game = []
            #  visit each player page, and make bs object
            for link in all_top_players[name]:
                soup = self.soup_page(link, headers, cookies)

                player_game_stats = \
                    soup.find_all('div', attrs={'class': 'palmares_game'})

                player_stats = []

                # makes the player database
                for ele in player_game_stats:
                    player_stats.append(ele.text)

                # makes the game database
                temp_stats_game.append(player_stats)

            # append each game database to the master raw database
            self.raw_players_stats[name] = [temp_stats_game, link]

        # see all the games whose top players are in the database
        print("Games in database: ",self.raw_players_stats.keys())

        return self.raw_players_stats

    def run_scraper(self):
        """ Call functions from throughout the package in
        order to fully scrape, clean and store the top player
        stats from BGA.

        Returns:
        --------
        5 JSON files of key data types, and the image associated
        with each game. The first two (*) will be useful for further
        analysis.

        * cleaned_player_stats.json
        * game_data.json
        all_top_players.json
        games_links.json
        raw_player_stats.json
        """

        print('Get games links')
        # If you fix the link gathering, change here
        # self.get_games_links()
        self.get_games_links_workaround()
        print('Log in')
        url = 'https://en.boardgamearena.com/account'
        self.log_in(url)
        time.sleep(2)

        print('Gather data')
        self.gather_game_data(self.link_list, self.game_data)
        self.get_images(self.game_data)
        self.raw_players_stats = \
            self.retrieve_player_stats(self.game_data, self.all_top_players)

        print('Clean data')
        self.all_game_stats = \
            cleaning.clean_player_stats(self.raw_players_stats)

        print('Save results')
        # make a directory for todays date
        date = datetime.today().strftime('%Y-%m-%d')
        newpath = f'./Data/{date}'
        if not os.path.exists(newpath):
            os.makedirs(newpath)

        # save results as json to directory
        self.save_results(
            self.all_top_players, f'./Data/{date}/all_top_players.json')
        self.save_results(
            self.game_data, './Data/game_data.json')
        self.save_results(
            self.link_list, f'./Data/{date}/games_links.json')
        self.save_results(
            self.raw_players_stats, f'./Data/{date}/raw_player_stats.json')
        self.save_results(
            self.all_game_stats, f'./Data/{date}/cleaned_player_stats.json')

if __name__ == "__main__":
    print('Data collection running...')
    t_0 = time.time()
    BGA = BGAscraper()
    BGA.run_scraper()
    print(f'Data collection took {time.time() - t_0} s')

    """Update AWS details in Cloud.py, then
    uncomment this code to push to the cloud"""

    # print("Save data to cloud...")
    # app = CloudIntegration()
    # app.save_to_s3()
    # app.dict_to_dataframes()
    # app.dataframes_to_aws()

    print('Done!')