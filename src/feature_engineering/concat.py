import pandas as pd

# simple script to concatenate entries of merged_df corresponding to the same game

merged_df = pd.read_csv('../../data/processed/merged.csv', index_col=0).sort_index()

# Initialize df from team A's perspective
df_A = merged_df.copy()

# rename columns to reflect team A's perspective
for col in df_A.columns:
    df_A.rename(columns={col: col + '_A'}, inplace=True)



# Initialize df from team B's perspective
df_B = pd.DataFrame(index=merged_df.index, columns = merged_df.columns)

# Switch even and odd entries
for i in merged_df.index:
    if i % 2 == 0:  # If index is even
        df_B.loc[i] = merged_df.loc[i + 1]  # Swap with the next row
    else:
        df_B.loc[i] = merged_df.loc[i - 1]  # Swap with the previous row
   
# rename columns to reflect team B's perspective
for col in df_B.columns:
    df_B.rename(columns={col: col + '_B'}, inplace=True)

# merge the two dataframes by game_id
total_df = pd.merge(df_A, df_B, left_index=True, right_index=True)

# clean up features that are the same for both teams (meta_cols)

meta_cols = ['GAME_DATE_EST', 'SEASON']
for col in meta_cols:
    total_df = total_df.drop(columns=col + '_B')
    total_df.rename(columns={col + '_A': col}, inplace=True)
    
# Save the concatenated dataset
total_df.to_csv('../../data/processed/total.csv', index=True)

