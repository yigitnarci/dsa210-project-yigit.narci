# google_trend_viz.py

import pandas as pd
import matplotlib.pyplot as plt

# 1) Load the CSVs
jersey     = pd.read_csv('jersey_ranks.csv')             # columns: Season, Player, Rank
trend_wide = pd.read_csv('combined_google_trends.csv')   # columns: date, <Player1>, <Player2>, …

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
trend['date'] = pd.to_datetime(trend['date'], errors='coerce')

def date_to_season(dt):
    # NBA season runs roughly Oct → Jun
    if dt.month >= 10:
        start, end = dt.year, dt.year + 1
    else:
        start, end = dt.year - 1, dt.year
    return f"{start}-{str(end)[2:]}"

trend['Season'] = trend['date'].apply(date_to_season)

# 5) Compute average TrendIndex per Season & Player
trend_avg = (
    trend
    .groupby(['Season','Player'], as_index=False)['TrendIndex']
    .mean()
)

# 6) (Optional) normalize jersey season formatting
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

# --- Output the merged TrendIndex table ---
print(f"Merged records: {len(df)}\n")
print(df.sort_values(['Season','Rank']).to_string(index=False))

# --- Scatter plot: Avg. TrendIndex vs. Jersey Rank ---
plt.figure(figsize=(10, 6))
x = df['TrendIndex']
y = df['Rank']

# invert y-axis so Rank=1 sits at the top
plt.gca().invert_yaxis()

# color‐code by season
categories = df['Season'].astype('category')
colors = categories.cat.codes
scatter = plt.scatter(x, y, c=colors, cmap='tab10', s=80, alpha=0.8)

# annotate each point with the player name
for _, row in df.iterrows():
    plt.text(row['TrendIndex'], row['Rank'],
             row['Player'],
             fontsize=8, ha='right', va='bottom')

plt.title("Average Google Trends vs. Jersey Rank")
plt.xlabel("Avg. Google Trends Index")
plt.ylabel("Jersey Rank (1 = top seller)")

# build a legend mapping seasons → colors
handles, _ = scatter.legend_elements(prop="colors")
labels = list(categories.cat.categories)
plt.legend(handles, labels, title="Season", bbox_to_anchor=(1.05,1), loc='upper left')

plt.tight_layout()
plt.show()
