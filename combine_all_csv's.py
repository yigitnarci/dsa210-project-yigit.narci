import pandas as pd

# 1. Load each dataset
df_jersey = pd.read_csv('jersey_ranks.csv')                       
df_stats = pd.read_csv('nba_top8_last5_cleaned_with_awards.csv')   
df_trends = pd.read_csv('avg_google_trends_by_season.csv')         
df_physical = pd.read_csv('final_players.csv')                     

# 2. Standardize column names
df_jersey.rename(columns={'Player': 'player_name', 'Rank': 'Jersey Rank'}, inplace=True)
df_stats.rename(columns={'Player': 'player_name'}, inplace=True)
df_trends.rename(columns={'Player': 'player_name'}, inplace=True)

# 3. Normalize season format (e.g., '2020-21' → '2020-2021')
season_map = {f"{y}-{str(y+1)[-2:]}": f"{y}-{y+1}" for y in range(2020, 2025)}
df_stats['Season'] = df_stats['Season'].map(season_map).fillna(df_stats['Season'])
df_jersey['Season'] = df_jersey['Season'].map(season_map).fillna(df_jersey['Season'])
df_trends['Season'] = df_trends['Season'].map(season_map).fillna(df_trends['Season'])

# 4. Merge stats and trends on player_name & Season
df_full = pd.merge(df_stats, df_trends, on=['player_name', 'Season'], how='left')

# 5. Merge with jersey ranks
df_full = pd.merge(
    df_full,
    df_jersey[['player_name', 'Season', 'Jersey Rank']],
    on=['player_name', 'Season'],
    how='left'
)

# 6. Merge with physical attributes on player_name
df_full = pd.merge(df_full, df_physical, on='player_name', how='left')

# 7. Feature Engineering: length & BMI
df_full['length'] = df_full['player_height']
df_full['BMI'] = df_full['player_weight'] / (df_full['player_height'] / 100) ** 2

# 8. Select and reorder columns
final_columns = [
    'Season', 'player_name', 'Jersey Rank',
    'Points/Game', 'Games Played', 'Minutes/Game', 'Award Count',
    'Google Trends Score', 'player_height', 'player_weight',
    'length', 'BMI'
]
df_final = df_full[final_columns]

# 9. Save the final enriched dataset
df_final.to_csv('full_enriched_dataset_with_bmi.csv', index=False)



