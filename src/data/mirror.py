import pandas as pd

# basic unique mapping from original index to mirror index
# * home team perspective is even
# * away team perspective is odd
def mirror_id_map(id, is_home):
    if is_home:
        return id * 2
    else:
        return id * 2 + 1

# Makes <mirror_df> out of the original dataframe, which contains the same data as 
# <df>, but each instance is replicated from the perspective of each team.
# In doing so:
# * column names are changed from 'stat_home' and 'stat_away' to 'stat_for' and 'stat_against'
# * game_id's are duplicated; home team perspective is even, away team perspective is odd
def make_mirror_df(df : pd.DataFrame) -> pd.DataFrame:
    
    # make mirror_df index
    index = df.index.sort_values()
    home_index = mirror_id_map(index, True)
    away_index = mirror_id_map(index, False)
    mirror_index = home_index.union(away_index).sort_values()
    
    # make mirror_df columns
    mirror_cols = ['TEAM_ID', 'GAME_DATE_EST', 'SEASON', 'TEAM_WINS'] 
    stat_cols = ['PTS', 'FG_PCT', 'FG3_PCT', 'AST', 'REB']
    for col in stat_cols:
        mirror_cols.append("{}_for".format(col))
        mirror_cols.append("{}_against".format(col))

    # initialize empty <mirror_df> 
    mirror_df = pd.DataFrame(index=mirror_index, columns=mirror_cols)
    
    
    for i, id in enumerate(df.index):
        if (i+1) % 1000 == 0: 
            print("Game {}/{}".format(i+1, len(df.index)))
        
        
        game = df.loc[id]
        
        # make data instance from home team perspective
        mirror_game_home = {col: None for col in mirror_cols}
        mirror_game_home['TEAM_ID'] = game['HOME_TEAM_ID']
        mirror_game_home['GAME_DATE_EST'] = game['GAME_DATE_EST']
        mirror_game_home['SEASON'] = game['SEASON']
        mirror_game_home['TEAM_WINS'] = game['HOME_TEAM_WINS']

        # stat data
        mirror_game_home['PTS_for'] = game['PTS_home']
        mirror_game_home['PTS_against'] = game['PTS_away']
        mirror_game_home['FG_PCT_for'] = game['FG_PCT_home']
        mirror_game_home['FG_PCT_against'] = game['FG_PCT_away']
        mirror_game_home['FG3_PCT_for'] = game['FG3_PCT_home']
        mirror_game_home['FG3_PCT_against'] = game['FG3_PCT_away']
        mirror_game_home['AST_for'] = game['AST_home']
        mirror_game_home['AST_against'] = game['AST_away']
        mirror_game_home['REB_for'] = game['REB_home']
        mirror_game_home['REB_against'] = game['REB_away']
        
        # make data instance from away team perspective
        mirror_game_away = {col: None for col in mirror_cols}
        mirror_game_away['TEAM_ID'] = game['VISITOR_TEAM_ID']
        mirror_game_away['GAME_DATE_EST'] = game['GAME_DATE_EST']
        mirror_game_away['SEASON'] = game['SEASON']
        mirror_game_away['TEAM_WINS'] = 1 - game['HOME_TEAM_WINS']

        # stat data
        mirror_game_away['PTS_for'] = game['PTS_away']
        mirror_game_away['PTS_against'] = game['PTS_home']
        mirror_game_away['FG_PCT_for'] = game['FG_PCT_away']
        mirror_game_away['FG_PCT_against'] = game['FG_PCT_home']
        mirror_game_away['FG3_PCT_for'] = game['FG3_PCT_away']
        mirror_game_away['FG3_PCT_against'] = game['FG3_PCT_home']
        mirror_game_away['AST_for'] = game['AST_away']
        mirror_game_away['AST_against'] = game['AST_home']
        mirror_game_away['REB_for'] = game['REB_away']
        mirror_game_away['REB_against'] = game['REB_home']
        
        # stash both into mirror_df using id mapping
        home_team_id = mirror_id_map(id, True)
        away_team_id = mirror_id_map(id, False)
        
        mirror_df.loc[home_team_id] = mirror_game_home
        mirror_df.loc[away_team_id] = mirror_game_away
    
    print("Done making mirror_df")
    
    return mirror_df
