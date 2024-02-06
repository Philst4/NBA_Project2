import pandas as pd

# Makes <streak_df> with same index as <mirror_df>, columns tracking stats over previous 'k' games, leading up to the corresponding game in <df>
# over prev 'k' games leading up to the corresponding game in <mirror_df>
# * Streaks only made using games from the same season
# * k = 0 -> streaks made using all previous games
def make_streak_df(mirror_df : pd.DataFrame, ks) -> pd.DataFrame:
    
    # Initializes empty <streak_df> 
    index = mirror_df.index
    old_cols = mirror_df.columns
    new_cols = []
    for k in ks:
        for col in old_cols:
            new_cols.append("{}_prev_{}".format(col, k))
            
    streak_df = pd.DataFrame(index=index, columns=new_cols)
    
    # Adds data to <streak_df> using streaks from the same season
    seasons = mirror_df['SEASON'].unique()
    
    for i, season in enumerate(seasons):
        print("Season {}/{}".format(i+1, len(seasons)))
        
        season_df = mirror_df[mirror_df['SEASON'] == season]
        teams = season_df['TEAM_ID'].unique()
        
        for j, team in enumerate(teams):
            print("Team {}/{}".format(j+1, len(teams)))
            
            team_df = season_df[season_df['TEAM_ID'] == team]
            team_df = team_df.sort_values(by='GAME_DATE_EST')
            
            for game in team_df.index:
                game_date = team_df.loc[game, 'GAME_DATE_EST']
                prev_games = team_df[team_df['GAME_DATE_EST'] < game_date]
                prev_games = prev_games.sort_values(by='GAME_DATE_EST', ascending=False)
                
                for k in ks:
                    if k == 0:
                        # Contains stats calculated from all previous games
                        prev_k_games = prev_games
                    else:
                        prev_k_games = prev_games.head(k)

                    # Calculate stats for previous k games
                    # Keep other column names in tact
                    stat_cols = ['PTS_for', 'PTS_ag',
                                 'FG_PCT_for', 'FG_PCT_ag', 
                                 'FG3_PCT_for', 'FG3_PCT_ag', 
                                 'AST_for', 'AST_ag', 
                                 'REB_for', 'REB_ag']
                    
                    for col in stat_cols:
                        streak_df.at[game, "{}_prev_{}".format(col, k)] = prev_k_games[col].mean()
                        
    
    return streak_df
    