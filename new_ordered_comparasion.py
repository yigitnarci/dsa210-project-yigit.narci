import pandas as pd

# 1) Load your raw per‐player file (with the original “Awards” column)
df = pd.read_csv('nba_top8_last5_by_player.csv')

# 2) Convert stat columns to numeric so we can sum/mean them
df['Games Played'] = pd.to_numeric(df['Games Played'],   errors='coerce')
df['Minutes/Game'] = pd.to_numeric(df['Minutes/Game'],    errors='coerce')
df['Points/Game']  = pd.to_numeric(df['Points/Game'],     errors='coerce')

# 3) Normalize the Awards column and build Award Count
df['Awards'] = df['Awards'].fillna('')  # replace NaN with empty string
# Treat any literal "No Awards" as empty
df.loc[df['Awards'].str.strip().str.lower() == 'no awards', 'Awards'] = ''

df['Award Count'] = (
    df['Awards']
      .str.split(',')
      .apply(lambda lst: sum(1 for award in lst if award.strip()))
)

# 4) Group by Season & Player, aggregating as requested
cleaned = (
    df
    .groupby(['Season','Player'], as_index=False)
    .agg({
        'Games Played': 'sum',    # sum games across multiple stints
        'Minutes/Game': 'mean',   # average minutes per game
        'Points/Game':  'mean',   # average points per game
        'Award Count':  'sum'     # total awards that season
    })
)

# 5) (Optional) sort for readability
cleaned = cleaned.sort_values(['Season','Games Played'], ascending=[True,False])

# 6) Write out the cleaned CSV
cleaned.to_csv('nba_top8_last5_cleaned_with_awards.csv', index=False)

# 7) Print a preview
print(cleaned)
