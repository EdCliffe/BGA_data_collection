#%%
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
import shutil

driver = webdriver.Chrome()
url = 'https://boardgamearena.com/gamepanel?game=azul'
drier = driver.get(url)


game_name_ele = driver.find_element_by_id("game_name")
game_details_ele = driver.find_element_by_class_name("col-md-6")


game_picture = driver.find_element_by_class_name('game_image')
picture_link = game_picture.get_attribute('src')
game_name = game_name_ele.text.lower()

print(game_name)
print(picture_link)
print(game_details_ele.text)


#%%
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
import shutil

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

# headers = None
# cookies = None
url = 'https://boardgamearena.com/'
page = requests.get(url, headers=headers, cookies=cookies)
html = page.text # Get the content of the webpage
soup = BeautifulSoup(html, 'html.parser')
print('soups up')


#%%
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import json
import shutil
import cleaning
driver = webdriver.Chrome()
url =  'https://boardgamearena.com/gamepanel?game=hanabi'


driver.get(url)
time.sleep(2)


game_name_ele = driver.find_element_by_id("game_name")
game_details_ele = driver.find_element_by_class_name("col-md-6")


game_picture = driver.find_element_by_class_name('game_image')
picture_link = game_picture.get_attribute('src')
game_name = game_name_ele.text.lower()
game_data = {}
all_top_players = {}
# clean details and add to dictionary
game_data[game_name] = cleaning.clean_games_stats(game_details_ele, game_data, game_name, picture_link,url)

# click extend, to see more players
xpath = '//*[@id="seemore"]'
try:
    driver.find_element_by_xpath(xpath).click()
except:
    pass
time.sleep(2)

# find player table
top_players = driver.find_element_by_class_name('gameranking')

# get each player from table, into list
top_player_list = top_players.find_elements_by_class_name('playername')

temp_players_list = []
# get each link from player, add the suffix to go to player stats page
for item in top_player_list:
    #link = item.find_element_by_tag_name('a')
    temp_players_list.append(item.get_attribute('href') + "&section=prestige")

# store in dictionary
temp_players_list.pop(0)
all_top_players[game_name] = temp_players_list




#%%

import json
import requests
from bs4 import BeautifulSoup
import requests

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

# response = requests.get('https://boardgamearena.com/', headers=headers, cookies=cookies)

with open('games_data.json', mode='r') as input:
    game_data = json.load(input)
with open('all_top_players.json', mode='r') as input:
        all_top_players = json.load(input)
raw_top_players_stats = {}
temp_stats_game = []
for name in game_data.keys():
    
    for link in all_top_players[name]:
        print(link)
        page = requests.get(link, headers=headers, cookies=cookies)
        html = page.text # Get the content of the webpage
        soup = BeautifulSoup(html, 'html.parser')
        print('trying to find stats')
        player_game_stats = soup.find_all('div', attrs={'class':'palmares_game'})
        player_stats = []
        # makes the player database
        for ele in player_game_stats:
            player_stats.append(ele.text)
        # makes the game database
        temp_stats_game.append(player_stats)

    raw_top_players_stats[name] = temp_stats_game
    
    

import json
import requests
from bs4 import BeautifulSoup
import requests
import time
game_stats = {}
player_stats = {}
all_game_stats = {}
# OPEN FILE, CLEAN THE DATA...
with open('all_top_players_stats.json', mode='r') as f:
    raw_player_stats = json.load(f)
    for k in raw_player_stats.keys():

        player_stats = {}
        for player in raw_player_stats[k]:
            for game_string in player:
                game_stat = []
                game_string = game_string.splitlines()
                #{player_name : {game name : [ELO, victories, games, win%]}
                player_name = game_string[-4].split("'")[0].strip()
                game_name = game_string[2].lower()
                elo = game_string[3].strip()
                victories = game_string[7].strip()
                victories = victories[0:-2]
                games = game_string[6].strip()
                games = games[0:-7]
                win_percent = game_string[8].strip()
                win_percent = win_percent[0:4]
                game_stat = [elo, victories, games, win_percent]
                print(game_stat)
                player_stats[game_name] = game_stat
            game_stats[player_name] = player_stats
        all_game_stats[k] = game_stats

with open('./Data/cleaned_player_stats.json', mode='w') as f:
    json.dump(all_game_stats, f)
       # player_stat = {player_name : {game_name : [elo, victories, games, win_percent]}}


#%%

import re

import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver 
from selenium.webdriver import ActionChains
import json


with open('games_links.json', mode='r') as f:
    links_list = json.load(f)
driver =  webdriver.Chrome()
for link in links_list:
            url = 'https://boardgamearena.com/' + link 
            print('gathering player links & game data')
            driver.get(url)
            game_name = driver.find_element_by_xpath('//*[@id="game_name"]').text
            print(game_name)
            game_details = driver.find_element_by_xpath('/*[@id="pageheader"]/div[3]/div[2]/div').text
            print(game_details)