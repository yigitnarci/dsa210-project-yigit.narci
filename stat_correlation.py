# stat_correlation_with_awards.py
import pandas as pd
from scipy.stats import spearmanr

# 1) Load both CSVs
jersey = pd.read_csv('jersey_ranks.csv')                            # Season, Player, Rank
perf   = pd.read_csv('nba_top8_last5_cleaned_with_awards.csv')      # Season, Player, Points/Game, Games Played, Minutes/Game, Award Count

# 2) Strip any extra whitespace
for df in (jersey, perf):
    df.columns   = df.columns.str.strip()
    df['Season'] = df['Season'].astype(str).str.strip()
    df['Player'] = df['Player'].astype(str).str.strip()

# 3) Normalize season strings like "2024-2025" → "2024-25"
def unify_season(s):
    s = s.replace('–','-')
    parts = s.split('-')
    if len(parts)==2 and len(parts[0])==4 and len(parts[1])==4:
        return parts[0] + '-' + parts[1][2:]
    return s

jersey['Season'] = jersey['Season'].apply(unify_season)
perf  ['Season'] = perf  ['Season'].apply(unify_season)

# 4) Merge: left‑join to preserve all jersey ranks
df = pd.merge(
    jersey[['Season','Player','Rank']],
    perf[['Season','Player','Points/Game','Games Played','Minutes/Game','Award Count']],
    on=['Season','Player'],
    how='left'
)

print(f"Merged records: {len(df)}  (should be 40 total)\n")
print(df.sort_values(['Season','Rank']).to_string(index=False))

# 5) Spearman correlations
metrics = {
    'Points/Game':   'PTS/Game',
    'Games Played':  'GP',
    'Minutes/Game':  'MPG',
    'Award Count':   'AWD'
}

print("\nSpearman correlations (ρ) of Rank vs. each metric:")
for col, short in metrics.items():
    sub = df.dropna(subset=[col, 'Rank'])
    rho, pval = spearmanr(sub['Rank'], sub[col])
    print(f"{short:>10} ↔ Rank : ρ = {rho:.3f},  p = {pval:.3f}")
