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

# --- 2) Merge to get exactly one row per (Season,Player) with PTS/Game & Rank ---
df = (
    pd.merge(
        jersey[['Season','Player','Rank']],
        stats [['Season','Player','Points/Game']],
        on=['Season','Player'],
        how='left'
    )
    # drop any rows missing Points/Game
    .dropna(subset=['Points/Game'])
)
# make sure types are numeric
df['Rank']       = df['Rank'].astype(int)
df['Points/Game']= df['Points/Game'].astype(float)

# --- 3) Build a 5‑panel FacetGrid, one column per season ---
sns.set(style='whitegrid')
g = sns.FacetGrid(
    df,
    col='Season',
    col_order=['2020-21','2021-22','2022-23','2023-24','2024-25'],
    col_wrap=5,        # force all 5 on one row
    height=4,
    sharex=False,      # allow different x‑ranges
    sharey=True        # keep rank scale the same
)

# scatter, coloring by season just so panels differ slightly
g.map_dataframe(
    sns.scatterplot,
    x='Points/Game',
    y='Rank',
    hue='Season',
    palette='tab10',
    s=80,
    legend=False
)

# annotate each point and tweak axes
for ax, (season, subdf) in zip(g.axes.flat, df.groupby('Season')):
    # invert y so rank=1 at the top
    ax.invert_yaxis()
    # annotate names
    for _, row in subdf.iterrows():
        ax.text(
            row['Points/Game'],
            row['Rank'],
            row['Player'],
            fontsize=8,
            verticalalignment='center',
            horizontalalignment='left'
        )
    # densify x‑ticks: up to 6 ticks
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    for lbl in ax.get_xticklabels():
        lbl.set_rotation(45)
        lbl.set_horizontalalignment('right')

# finish up
g.set_axis_labels('PTS/Game', 'Jersey Rank (1=top seller)')
g.fig.suptitle('PTS/Game vs. Jersey Rank by Season', y=1.02)
plt.tight_layout()
plt.show()
