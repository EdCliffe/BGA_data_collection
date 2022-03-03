# %% Upload all images to AWS S3 bucket
from ast import While
import boto3
import json
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import numpy as np
if __name__ == "__main__":
    
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

    for file in my_bucket.objects.all():
        print(file.key)
    print('done')


# %%
from datetime import datetime
import json
import pandas as pd
import numpy as np
date = datetime.today().strftime('%Y-%m-%d')

with open('../project/Data/games_links.json', mode='r') as f:
    games_links = json.load(f)

with open(f'../project/Data/{date}/all_top_players.json', mode='r') as f:
    all_top_players = json.load(f)

with open('../project/Data/game_data.json', mode='r') as f:
    game_data = json.load(f)

with open(f'../project/Data/{date}/cleaned_player_stats.json', mode='r') as f:
    cleaned_player_stats = json.load(f)

with open(f'../project/Data/{date}/raw_player_stats.json', mode='r') as f:
    raw_player_stats = json.load(f)

pd_game_links = pd.DataFrame(games_links)
pd_all_top_players = pd.DataFrame(all_top_players)
pd_game_data = pd.DataFrame(game_data)

# for game_name in cleaned_player_stats.keys():

#     pd_cleaned_player_stats.loc[cleaned_player_stats[game_name]]
# pd_cleaned_player_stats.head()
# table 1 = game name / top player names
player_table = {}
game_list = []
player_list = []

for i in cleaned_player_stats.keys():
    game_list.append(i)

for j in game_list:
    temp = cleaned_player_stats[j].keys()
    temp_players = []
    for k in temp:
        temp_players.append(k)
    player_list.append(temp_players)

master_list = {}
pd_player_table = pd.DataFrame(player_list, game_list).T
played_games = {}
master_player_dict = {}
# create a dictionary of each player and the games they have played
for game in game_list:
    for item in cleaned_player_stats[game]:
        # print(item)
        player_key_list = []
        for i in cleaned_player_stats[game][item].keys():
            player_key_list.append(i)
        master_player_dict[item] = player_key_list
# append None to make square table
for i in master_player_dict.keys():
    while len(master_player_dict[i]) < 20:
        master_player_dict[i].append(None)

# dataframe of all player names with the games they played
pd_player_games = pd.DataFrame(master_player_dict)

# all player stats stored in a dictionary of dataframes
# add each dataframe to the database in a loop
df_dict = {}
for game in game_list:
    player_keys = cleaned_player_stats[game].keys()
    for key in player_keys:
        df_dict[key] = pd.DataFrame(cleaned_player_stats[game][key], ['ELO','wins','games_played']).T
        # df_dict[key].to_sql(f'{key}', engine, if_exists='replace')
        # TODO check best way to store these thousands of tables, 
        # which increase in number every week...

#print(master_player_dict)
#print('done')


# %%

from ast import While
import boto3
import json
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime
import numpy as np

DATABASE_TYPE = 'postgresql'
DBAPI = 'psycopg2'
ENDPOINT = 'aicoredb.cmrvtkhfvvfh.us-east-1.rds.amazonaws.com' # Change it for your AWS endpoint
USER = 'postgres'
PASSWORD = 'Fooqlzj3'
PORT = 5432
DATABASE = 'BGA_Scraper'
engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}")

engine.connect()
pd_player_games.to_sql('player_games', engine, if_exists='replace')
pd_game_links.to_sql('game_links', engine, if_exists='replace')
pd_all_top_players.to_sql('all_top_players', engine, if_exists='replace')
pd_game_data.to_sql('game_data', engine, if_exists='replace')
pd_player_table.to_sql('player_table', engine, if_exists='replace')

for key in df_dict.keys():
    df_dict[key].to_sql(f'{key}', engine, if_exists='replace')
print('done')