# %%
# import json
# from datetime import datetime
import re


def clean_games_stats(game_details_ele, picture_link, url):
    """
    This module contains functions for cleaning data,
    it is called by BGA_scraper when run.
    Keyword arguements:
    -------------------
    game_details - game info to be cleaned, string
    picture_link - url to game image, passed on without cleaning
    url - url to game page, passed on without cleaning

    Returns:
    --------
    players - number of players required
    playtime_cleaned - aproximate playtime in minutes
    complexity - game complexity ranked from 1 (lowest) to 5 (highest)
    picture_link - url for the game image, to be downloaded later
    url - url to game page, for reference
    """
    game_details = game_details_ele.text
    game_details = game_details.split('\n')
    game_details = game_details[1]

    players = game_details[0:5]
    playtime = game_details[8:12]
    playtime_cleaned = playtime.split()
    playtime_cleaned = playtime_cleaned[0]
    complexity = game_details[-5:]

    # add to dictionary in BGA_scraper
    return [players, playtime_cleaned, complexity, picture_link, url]


def clean_player_stats(raw_players_stats):
    """Cleans the gathered player stats in a deep nested fashion.

    Keyword arguments:
    ------------------
    raw_player_stats - dict
        raw_player_stats[game_name] =
        [['single_player_stats_for_all_games']... [] ]

    Returns:
    --------
    cleaned_player_stats - dict
        cleaned_player_stats['game_name'] =
        {game_name:
        {player_name:
        [ {game_name: [[ELO, victories, games played, win_%], player_url] } ]}}

        Contains game_name as index twice,
        as each player plays many different games,
        not just the one they are in the league table for.
        allows the best players of each game to be compared
        for their non-best games also.
        """

    all_game_stats = {}

    for k in raw_players_stats.keys():       # for each game..
        game_stats = {}
        for player in raw_players_stats[k][0]:  # ..there are many players..
            player_stats = {}
            i = 0
            for game_string in player:    # .. and each player, has many stats.

                game_stat = []

                # split on spaces,
                # then divide assign the resulting list to variables
                game_string = game_string.splitlines()

                player_name = game_string[-4].split("'")[0].strip()
                game_name = game_string[2].lower()
                elo = game_string[3][0:3].strip()

                victories = game_string[7].strip()
                victories = "".join(victories.split())
                victories = victories[0:5].strip()
                victories = re.sub('\D',"", victories)

                games = game_string[6].strip()
                games = games[0:5].strip()
                games = "".join(games.split())
                games = re.sub('\D',"", games)

                # assign temporary variables to desired structures
                # before next iteration
                game_stat = [elo, victories, games]
                player_stats[game_name] = game_stat

                i += 1
                if i == 20:
                    break

            game_stats[player_name] = [player_stats, raw_players_stats[k][1]]
        all_game_stats[k] = game_stats
    return all_game_stats

# date = datetime.today().strftime('%Y-%m-%d')

# with open(f'./Data/{date}/raw_player_stats.json', mode='r') as f:
#     raw_player_stats = json.load(f)
# clean_player_stats(raw_player_stats)
