import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr
import matplotlib.pyplot as plt
import seaborn as sns

# 1) Load
jersey = pd.read_csv('jersey_ranks.csv')              # Season, Rank, Player
trend  = pd.read_csv('combined_google_trends.csv')    # date + one column per player

# 2) Clean up column names & player typos
trend.rename(columns={'Stephan Curry': 'Stephen Curry'}, inplace=True)
trend.columns = trend.columns.str.strip()
jersey['Player'] = jersey['Player'].str.strip()
jersey['Season'] = jersey['Season'].str.strip()

# 3) Compute season label for each weekly row
trend['date'] = pd.to_datetime(trend['date'])
def to_season(dt):
    year, m = dt.year, dt.month
    if m >= 10:
        start, end = year, year + 1
    else:
        start, end = year - 1, year
    return f"{start}-{str(end)[2:]}"
trend['Season'] = trend['date'].apply(to_season)

# 4) Melt to long form and average per season/player
value_cols = [c for c in trend.columns if c not in ['date','Season']]
_long = trend.melt(id_vars=['Season'], value_vars=value_cols,
                   var_name='Player', value_name='TrendIndex')
_avg_tr = (_long
    .groupby(['Season','Player'], as_index=False)['TrendIndex']
    .mean()
    .rename(columns={'TrendIndex':'AvgTrendIndex'})
)

# 5) Make jersey seasons match the same “YYYY-YY” format
def unify_jseason(s):
    # e.g. “2024-2025” → “2024-25”
    p = s.split('-')
    if len(p)==2 and len(p[1])==4:
        return p[0] + '-' + p[1][2:]
    return s

jersey['Season'] = jersey['Season'].apply(unify_jseason)

# 6) Merge and drop any missing trend rows
df = (jersey
      .merge(_avg_tr, on=['Season','Player'], how='inner')
      .dropna(subset=['AvgTrendIndex','Rank'])
)
print(f"Merged records: {len(df)} (should be 40)\n")
print(df.sort_values(['Season','Rank']).to_string(index=False))

# 7) Compute correlations
rho_s, p_s = spearmanr(df['Rank'], df['AvgTrendIndex'])
rho_p, p_p = pearsonr(df['Rank'], df['AvgTrendIndex'])
print("\n--- Correlation results ---")
print(f"Spearman ρ = {rho_s:.3f},  p = {p_s:.3f}")
print(f"Pearson  ρ = {rho_p:.3f},  p = {p_p:.3f}")

# 8) Plot
plt.figure(figsize=(6,5))
sns.regplot(
    data=df,
    x='AvgTrendIndex', y='Rank',
    scatter_kws={'s': 80, 'alpha':0.8},
    line_kws={'color':'crimson'}
)
plt.gca().invert_yaxis()  # so rank=1 sits at the top
plt.title('Google Trends vs. Jersey Rank')
plt.xlabel('Average Google Trends Index')
plt.ylabel('Jersey Rank (1 = top seller)')
plt.tight_layout()
plt.show()
