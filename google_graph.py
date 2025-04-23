# google_correlation.py
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import spearmanr, pearsonr

# 1) Load the CSVs
jersey = pd.read_csv('jersey_ranks.csv')             # columns: Season, Player, Rank
trend_wide = pd.read_csv('combined_google_trends.csv')  # columns: date, <Player1>, <Player2>, …

# 2) Clean up column names
for df in (jersey, trend_wide):
    df.columns = df.columns.str.strip()

# 3) Melt the Trends DF to long form
trend = trend_wide.melt(
    id_vars=['date'],
    var_name='Player',
    value_name='TrendIndex'
)

# 4) Parse dates and bucket into seasons
trend['date'] = pd.to_datetime(trend['date'])

def date_to_season(dt):
    # NBA season runs roughly Oct → Jun:
    # Oct–Dec → season starts that year; Jan–Jun → season started previous year
    if dt.month >= 10:
        start = dt.year
        end   = dt.year + 1
    else:
        start = dt.year - 1
        end   = dt.year
    return f"{start}-{str(end)[2:]}"

trend['Season'] = trend['date'].apply(date_to_season)

# 5) Compute average TrendIndex per Season & Player
trend_avg = (
    trend
    .groupby(['Season','Player'], as_index=False)['TrendIndex']
    .mean()
)

# 6) (Optionally) normalize formatting of jersey seasons too
def unify_season(s):
    s = s.replace('–','-')
    parts = s.split('-')
    if len(parts)==2 and len(parts[0])==4 and len(parts[1])==4:
        return parts[0] + '-' + parts[1][2:]
    return s

jersey['Season'] = jersey['Season'].astype(str).apply(unify_season)
jersey['Player'] = jersey['Player'].astype(str).str.strip()

# 7) Merge on Season & Player (inner join to keep only matched rows)
df = pd.merge(
    jersey[['Season','Player','Rank']],
    trend_avg,
    on=['Season','Player'],
    how='inner'
)

print(f"​Merged records: {len(df)}  (should match number of ranked players with trend data)\n")
print(df.sort_values(['Season','Rank']).to_string(index=False))

# 8) Run correlations
spearman_rho, spearman_p = spearmanr(df['Rank'], df['TrendIndex'])
pearson_r,   pearson_p   = pearsonr(df['Rank'], df['TrendIndex'])

print("\n--- Correlation results ---")
print(f"Spearman ρ = {spearman_rho:.3f},  p‐value = {spearman_p:.3f}")
print(f"Pearson  ρ = {pearson_r:.3f},  p‐value = {pearson_p:.3f}")

# 9) Scatter plot with annotations
plt.figure(figsize=(8,6))
x = df['TrendIndex']
y = df['Rank']

# because Rank=1 is top seller & plotting downward:
plt.gca().invert_yaxis()

scatter = plt.scatter(x, y, s=80, c=df['Season'].astype('category').cat.codes, cmap='tab10', alpha=0.8)
for _, row in df.iterrows():
    plt.text(row['TrendIndex'], row['Rank'],
             row['Player'], fontsize=8, ha='right', va='bottom')

plt.title("Avg. Google Trends vs. Jersey Rank")
plt.xlabel("Average TrendIndex (per season)")
plt.ylabel("Jersey Rank (1 = top seller)")

# build legend mapping seasons → colors
handles, _ = scatter.legend_elements(prop="colors")
labels = list(df['Season'].astype('category').cat.categories)
plt.legend(handles, labels, title="Season", bbox_to_anchor=(1.05,1), loc='upper left')

plt.tight_layout()
plt.show()
