#%%  SECTIONS FOR ACCESSING and playing with SAVED DATABASE
import json
from datetime import datetime

date = datetime.today().strftime('%Y-%m-%d')
with open(f'./Data/{date}/cleaned_player_stats.json', mode='r') as f:
    stats = json.load(f)
print((stats['carcassonne']['RabbitRain'][0]))
#%%


with open(f'./Data/game_data.json', mode='r') as f:
    game_data = json.load(f)
print(len(game_data))

#%%
import json
with open(f'./Data/{date}/all_top_players.json', mode='r') as f:
    top_players = json.load(f)
print(top_players)
#%%
with open(f'./Data/{date}/raw_player_stats.json', mode='r') as f:
    stats = json.load(f)
print(stats['azul'])
#%%
import json
with open(f'./Data/{date}/games_links.json', mode='r') as f:
    stats = json.load(f)
print(len(stats))

