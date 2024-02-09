# simple script to merge mirror.py and streak.py via their game indices


# IMPORTS

import pandas as pd

mirror_df = pd.read_csv('../../data/processed/mirror.csv', index_col=0)
streak_df = pd.read_csv('../../data/processed/streak.csv', index_col=0)

# Find and drop overlapping features
overlapping_features = list(set(mirror_df.columns) & set(streak_df.columns))
for feature in overlapping_features:
    if mirror_df[feature].equals(streak_df[feature]):
        streak_df = streak_df.drop(columns=feature)

# Select features from both datasets, merge
merged_df = pd.merge(mirror_df, streak_df, left_index=True, right_index=True)

# Add whether or not the game was a home game
merged_df['IS_HOME'] = merged_df.index % 2 == 0

# Save the merged dataset
merged_df.to_csv('../../data/processed/merged.csv', index=True)

print("Done merging datasets")