# %% Upload all images to AWS S3 bucket
import boto3
import json
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime


class CloudIntegration():
    def __init__(self) -> None:
        pass

    def save_to_s3(self):
        """Save images to S3 bucket"""

        s3_client = boto3.client('s3')

        # response = s3_client.upload_file(file_name, bucket, object_name)

        with open('./Data/game_data.json', mode='r') as f:
            game_data = json.load(f)

        for name in game_data.keys():
            filename = name + '.jpg'
            response = s3_client.upload_file(
                f'./Data/Images/{filename}', 'bgascraper', filename)

        # report the files which are in the S3 bucket
        s3 = boto3.resource('s3')

        my_bucket = s3.Bucket('bgascraper')

        # for file in my_bucket.objects.all():
        #     print(file.key)

        return print('Saved images to S3 bucket')

# 450        x 20         x between 5-20 x1 
# {game_name: {player_name: [{game_name: [ELO, victories, games played, win_%], player url]}}
# player_name : player_urls - potentially 9000 row 2 columns
# _/ player_name : long stat string : url - potentially 9000 row, 3 columns

    def dict_to_dataframes(self):

        date = datetime.today().strftime('%Y-%m-%d')
        # date = "2022-03-03"
        # list of 450 urls
        """Load data to store in RDS"""
        with open('../project/Data/games_links.json', mode='r') as f:
            self.games_links = json.load(f)

            # dictionary, game name / list of player urls
        with open(f'../project/Data/{date}/all_top_players.json', mode='r') as f:
            self.all_top_players = json.load(f)

            # dictionary, game name / players, time, complexity, image link, game_link
        with open('../project/Data/game_data.json', mode='r') as f:
            self.game_data = json.load(f)

        with open(f'../project/Data/{date}/cleaned_player_stats.json', mode='r') as f:
            self.cleaned_player_stats = json.load(f)

        with open(f'../project/Data/{date}/raw_player_stats.json', mode='r') as f:
            self.raw_player_stats = json.load(f)

        """Process stored data into pandas dataframes"""
        self.pd_game_links = pd.DataFrame(self.games_links)
        self.pd_game_data = pd.DataFrame(self.game_data)

        """Create dataframe relating the game name to the players
        who are in the top 20 list of that game"""
        game_list = []
        player_list = []

        for i in self.cleaned_player_stats.keys():
            game_list.append(i)

        for j in game_list:
            temp = self.cleaned_player_stats[j].keys()
            temp_players = []
            for k in temp:
                temp_players.append(k)
            player_list.append(temp_players)

        self.pd_player_table = pd.DataFrame(player_list, game_list).T
        master_player_dict = {}

        """Create a dictionary of the of all gathered player
        names with the all of the games they have played,
        not just their top game"""

        for game in game_list:
            for player in self.cleaned_player_stats[game]:
                player_key_list = []
                for i in self.cleaned_player_stats[game][player][0].keys():
                    player_key_list.append(i)
                    # player_key_list is a list of all the games each player has played

                master_player_dict[player] = player_key_list
        # append None to make square table
        for i in master_player_dict.keys():
            while len(master_player_dict[i]) < 20:
                master_player_dict[i].append(None)

        # this is a DF of the top 20 games each player has played
        self.pd_player_games = pd.DataFrame(master_player_dict)

        """ Create dictionary to store players game stats
        with their name as key, stats as a string,
        and url included for reference"""

        player_stats_dict = {}

        for game in game_list:

            player_keys = self.cleaned_player_stats[game].keys()
            for player in player_keys:
                player_stats_dict[player] = \
                    [str(self.cleaned_player_stats[game][player][0]),
                     self.cleaned_player_stats[game][player][1]]

        # all player stats stored as a string,
        # with the player name and url as reference
        self.df_players_stats = \
            pd.DataFrame.from_dict(data=(player_stats_dict),  orient='index')

        return print("Processed data into dataframes")



    def dataframes_to_aws(self):
        """ Send dataframes to AWS hosted SQL RDS"""

        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        ENDPOINT = 'aicoredb.cmrvtkhfvvfh.us-east-1.rds.amazonaws.com'
        USER = 'postgres'
        PASSWORD = 'Fooqlzj3'
        PORT = 5432
        DATABASE = 'BGA_Scraper'
        engine = \
        create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")

        engine.connect()
        self.pd_player_games.to_sql('player_games', engine, if_exists='replace')
        self.pd_game_links.to_sql('game_links', engine, if_exists='replace')
        self.pd_game_data.to_sql('game_data', engine, if_exists='replace')
        self.pd_player_table.to_sql('player_table', engine, if_exists='replace')
        self.df_players_stats.to_sql('player_stats', engine, if_exists='replace')

        # for key in df_dict.keys():
        #     df_dict[key].to_sql(f'{key}', engine, if_exists='replace')
        return print('Sent dataframes to postgres')


if __name__ == "__main__":

    