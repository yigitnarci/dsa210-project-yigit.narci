import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- 1) Load & clean up your CSVs ---
jersey = pd.read_csv('jersey_ranks.csv')  
stats  = pd.read_csv('nba_top8_last5_cleaned_with_awards.csv')

# strip whitespace
for df in (jersey, stats):
    df.columns = df.columns.str.strip()
    df['Season'] = df['Season'].astype(str).str.strip()
    df['Player'] = df['Player'].astype(str).str.strip()

# unify season formatting: "2024-2025" → "2024-25"
def unify_season(s):
    s = s.replace('–','-')
    parts = s.split('-')
    if len(parts)==2 and len(parts[0])==4 and len(parts[1])==4:
        return f"{parts[0]}-{parts[1][2:]}"
    return s

jersey['Season'] = jersey['Season'].apply(unify_season)
stats ['Season'] = stats ['Season'].apply(unify_season)

# --- 2) Merge to get one row per (Season,Player) with Games Played & Rank ---
df = (
    pd.merge(
        jersey[['Season','Player','Rank']],
        stats [['Season','Player','Games Played']],
        on=['Season','Player'],
        how='left'
    )
    .dropna(subset=['Games Played'])
)

df['Rank']         = df['Rank'].astype(int)
df['Games Played'] = df['Games Played'].astype(float)

# --- 3) Build a FacetGrid of 5 side‑by‑side panels ---
sns.set(style='whitegrid')
g = sns.FacetGrid(
    df,
    col='Season',
    col_order=['2020-21','2021-22','2022-23','2023-24','2024-25'],
    col_wrap=5,
    height=4,
    sharex=False,
    sharey=True
)

# scatterplot colored by season
g.map_dataframe(
    sns.scatterplot,
    x='Games Played',
    y='Rank',
    hue='Season',
    palette='tab10',
    s=80,
    legend=False
)

# annotate & format each panel
for ax, (season, subdf) in zip(g.axes.flat, df.groupby('Season')):
    ax.invert_yaxis()  # rank=1 at top
    # annotate names
    for _, row in subdf.iterrows():
        ax.text(
            row['Games Played'],
            row['Rank'],
            row['Player'],
            fontsize=8,
            va='center',
            ha='left'
        )
    # densify x‑axis ticks
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    for lbl in ax.get_xticklabels():
        lbl.set_rotation(45)
        lbl.set_horizontalalignment('right')

# labels & title
g.set_axis_labels('Games Played', 'Jersey Rank (1=top seller)')
g.fig.suptitle('Games Played vs. Jersey Rank by Season', y=1.02)
plt.tight_layout()
plt.show()
