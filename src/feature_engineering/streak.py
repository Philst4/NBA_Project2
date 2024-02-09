import pandas as pd
import time


# Makes the column names for <streak_df> using mirror_df's columns
# * Stat columns are renamed to include '_prev_k' for each k in <ks>
def make_streak_col(col, k):
    return "{}_prev_{}".format(col, k)


# Makes <streak_df> with same index as <mirror_df>, columns tracking stats over previous 'k' games, leading up to the corresponding game in <df>
# over prev 'k' games leading up to the corresponding game in <mirror_df>
# * Streaks only made using games from the same season
# * k = 0 -> streaks made using all previous games
def make_streak_df(mirror_df : pd.DataFrame, ks) -> pd.DataFrame:
    
    meta_cols = ['TEAM_ID', 'GAME_DATE_EST', 'SEASON']
    
    are_stat_cols = ~mirror_df.columns.isin(meta_cols)
    old_stat_cols = mirror_df.columns[are_stat_cols]
    
    new_stat_cols = []
    for k in ks:
        for col in old_stat_cols:
            streak_col = make_streak_col(col, k)
            new_stat_cols.append(streak_col)
    
    # Initializes empty <streak_df>, same index as <mirror_df>
    index = mirror_df.index
    new_cols = meta_cols + new_stat_cols
    streak_df = pd.DataFrame(index=index, columns=new_cols)
    
    # Adds data to <streak_df> using streaks from the same season
    print("k values: {}".format(ks))
    print("features: {}".format(new_cols))
    
    
    # Sort <streak_df> by season
    streak_df = streak_df.sort_values(by='SEASON')
    seasons = mirror_df['SEASON'].unique()
    
    for i, season in enumerate(seasons):
        print("Season {}/{}".format(i+1, len(seasons)))
        
        # Make a df for the current season, sort by team
        season_df = mirror_df[mirror_df['SEASON'] == season]
        season_df.sort_values(by='TEAM_ID')
        
        teams = season_df['TEAM_ID'].unique()
        
        for j, team in enumerate(teams):
            print("Team {}/{}".format(j+1, len(teams)))
            
            # Make a df for the current team, sort by date
            team_df = season_df[season_df['TEAM_ID'] == team]
            team_df = team_df.sort_values(by='GAME_DATE_EST')
            
            for game in team_df.index:
                game_date = team_df.loc[game, 'GAME_DATE_EST']
                prev_games = team_df[team_df['GAME_DATE_EST'] < game_date]
                prev_games = prev_games.sort_values(by='GAME_DATE_EST', ascending=False)
                
                # add stat col data to <streak_df>
                for k in ks:
                    if k == 0:
                        # Contains stats calculated from all previous games
                        prev_k_games = prev_games
                    else:
                        prev_k_games = prev_games.head(k)
                    
                    for col in old_stat_cols:
                        streak_col = make_streak_col(col, k)
                        streak_df.at[game, streak_col] = prev_k_games[col].mean()
                
                # add meta col data to <streak_df>
                for col in meta_cols:
                    streak_df.at[game, col] = team_df.at[game, col]   

    return streak_df


# Makes <streak_df> of streak data with, same index as <mirror_df>,
# columns tracking stats over previous 'k' games, leading up to 
# the corresponding game in <df>

start = time.time()

mirror_df = pd.read_csv('../../data/processed/mirror.csv', index_col=0)


ks = [0, 1, 3, 5, 10, 20]
streak_df = make_streak_df(mirror_df, ks)

streak_df.to_csv('../../data/processed/streak.csv', index=True)

end = time.time()

print(end - start, "seconds")