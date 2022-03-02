#%%
import unittest
import os, os.path
import json

# TODO test for website changes?
# find tests for selenium processes

class TestBGA(unittest.TestCase):
    def setUp(self) -> None:

        with open('../Scraper/Data/games_links.json', mode='r') as f:
            self.games_links = json.load(f)

        with open('../Scraper/Data/all_top_players.json', mode='r') as f:
            self.all_top_players = json.load(f)
        
        with open('../Scraper/Data/game_data.json', mode='r') as f:
            self.game_data = json.load(f)

        with open('../Scraper/Data/cleaned_player_stats.json', mode='r') as f:
            self.cleaned_player_stats = json.load(f)

        with open('../Scraper/Data/raw_player_stats.json', mode='r') as f:
            self.raw_player_stats = json.load(f)


    def test_game_links(self):

        # test is list of links, 
        self.assertIsInstance(self.games_links, list)

        # where each link starts with a /gamepanel?game=
        for link in self.games_links:
            self.assertEqual(link[0:16], '/gamepanel?game=')


    def test_all_top_players(self):
        # is a dictionary
        atp = self.all_top_players
        self.assertIsInstance(atp, dict)

        for k in atp.keys():
            # which contains a list for every entry            
            self.assertIsInstance(atp[k], list)
            # 20 players for every game
            try:
                self.assertEqual(len(atp[k]), 20)
            except AssertionError:
                self.assertEqual(len(atp[k]), 19)


            # all players unique
            try:
                self.assertEqual(len(set(atp[k])), 20)
            except AssertionError:
                self.assertEqual(len(set(atp[k])), 19)


        # each link starts with https://boardgamearena.com/
        # and ends with  section=prestige
            for link in atp[k]:
                self.assertEqual(link[0:31], "https://boardgamearena.com/play")
                self.assertEqual(link[-16:], "section=prestige")

    def test_game_data(self):
        # eg ['2 - 4', '14', '1 / 5', 'https://x.boardgamearena.net/data/themereleases/220215-1000/games/azul/220223-1845/img/game_box.png', 'https://boardgamearena.com/gamepanel?game=azul']
        gd = self.game_data
        for k in gd.keys():
            self.assertIsInstance(gd[k], list)  # is a list
            self.assertEqual(len(gd[k]), 5)  # with 5 items
            for ele in gd[k]:
                self.assertIsInstance(ele, str)  # list contains strings
            # two of which are links
            self.assertEqual(gd[k][3][0:34], 'https://x.boardgamearena.net/data/')
            self.assertEqual(gd[k][4][0:36], 'https://boardgamearena.com/gamepanel')
        # as many groups of players as there are sets of game data
        self.assertEqual(len(self.game_data), len(self.all_top_players))

    def test_images(self):
    # should be as many images in data folder as there are games data lists
        how_many_images = \
            len([name for name in os.listdir('../Scraper/Data/Images')])
        self.assertEqual(how_many_images, len(self.game_data.keys()))

    def test_raw_player_stats(self):
        # should be 20 players stat lists per game, len(stats['azul'])) == 20
        rps = self.raw_player_stats
        for k in rps.keys():
            try:
                self.assertEqual(len(rps[k]), 20)
            except AssertionError:
                self.assertEqual(len(rps[k]), 19)

    
    def test_cleaned_player_stats(self):
        # cleaned_player_stats format
        # {game_name : {player_name: {game_name:[ELO, victories, games played, win_percent]]}}

        cps = self.cleaned_player_stats

         # as many games headings as there are links to games
        self.assertEqual(len(cps.keys()), (len(self.games_links)-1))  # -1 for Hanabi
        # checking types, dictionary structure
        total_data = 0
        for k in cps.keys():  # game names
            self.assertIsInstance(cps[k], dict)
            total_data += len(cps[k].keys())
            for j in cps[k].keys():  # player_names
                self.assertIsInstance(cps[k][j], dict)
                for i in cps[k][j].keys(): # game_names
                    self.assertIsInstance(cps[k][j][i], list)
                    self.assertEqual(len(cps[k][j][i]), 4)

        total_list = 0
        # total players in list
        for k in self.all_top_players.keys():
            total_list += len(self.all_top_players[k])
        # total players in database calcd above
        # number of players in cleaned_player_stats  == 
        # sum of all players in all games in all_top_players
        self.assertEqual(total_list, total_data)


# def tearDown(self):
#     del self.

unittest.main(argv=[''], verbosity=0, exit=False)