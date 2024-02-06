import pandas as pd 

# local imports
from utils import make_mirror_df, make_streak_df

# Load data
df = pd.read_csv('../../data/raw/games.csv')

# Drop columns that are not needed
df.drop('GAME_STATUS_TEXT', axis=1, inplace=True)

# Convert GAME_DATE_EST to datetime
df['GAME_DATE_EST'] = pd.to_datetime(df['GAME_DATE_EST'])

# Make 'GAME_ID' the index
df = df.drop_duplicates(subset='GAME_ID') # drop conflicing rows
df.set_index('GAME_ID', inplace=True)

# Make mirror_df
mirror_df = make_mirror_df(df)

# makes streak data
streak_df = make_streak_df(mirror_df, [5, 10, 20])

print(streak_df.head(6))