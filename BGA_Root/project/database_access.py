#%%  SECTIONS FOR ACCESSING and playing with SAVED DATABASE
import json
with open('./Data/cleaned_player_stats.json', mode='r') as f:
    stats = json.load(f)
print((stats['azul'].keys()))
#%%

with open('./Data/game_data.json', mode='r') as f:
    game_data = json.load(f)
print(len(game_data))

#%%
import json
with open('./Data/all_top_players.json', mode='r') as f:
    top_players = json.load(f)
print(top_players)
#%%
with open('./Data/raw_player_stats.json', mode='r') as f:
    stats = json.load(f)
print(len(stats['azul']))
