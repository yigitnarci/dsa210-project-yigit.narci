import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- 1) Load & clean your CSVs ---
jersey = pd.read_csv('jersey_ranks.csv')  
stats  = pd.read_csv('nba_top8_last5_cleaned_with_awards.csv')

# strip whitespace
for df in (jersey, stats):
    df.columns = df.columns.str.strip()
    df['Season'] = df['Season'].astype(str).str.strip()
    df['Player'] = df['Player'].astype(str).str.strip()

# unify season formatting
def unify_season(s):
    s = s.replace('–','-')
    parts = s.split('-')
    if len(parts)==2 and len(parts[0])==4 and len(parts[1])==4:
        return f"{parts[0]}-{parts[1][2:]}"
    return s

jersey['Season'] = jersey['Season'].apply(unify_season)
stats ['Season'] = stats ['Season'].apply(unify_season)

# --- 2) Merge to one row per (Season,Player) with Minutes/Game & Rank ---
df = (
    pd.merge(
        jersey[['Season','Player','Rank']],
        stats [['Season','Player','Minutes/Game']],
        on=['Season','Player'],
        how='left'
    )
    .dropna(subset=['Minutes/Game'])
)

df['Rank']         = df['Rank'].astype(int)
df['Minutes/Game'] = df['Minutes/Game'].astype(float)

# --- 3) Build a FacetGrid (5 panels) ---
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
    x='Minutes/Game',
    y='Rank',
    hue='Season',
    palette='tab10',
    s=80,
    legend=False
)

# annotate & format each subplot
for ax, (season, subdf) in zip(g.axes.flat, df.groupby('Season')):
    ax.invert_yaxis()  # so Rank=1 is at top
    # annotate player names
    for _, row in subdf.iterrows():
        ax.text(
            row['Minutes/Game'],
            row['Rank'],
            row['Player'],
            fontsize=8,
            va='center',
            ha='left'
        )
    # make x‐ticks denser and rotate labels
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
    for lbl in ax.get_xticklabels():
        lbl.set_rotation(45)
        lbl.set_horizontalalignment('right')

# axis labels & overall title
g.set_axis_labels('Minutes per Game', 'Jersey Rank (1=top seller)')
g.fig.suptitle('Minutes/Game vs. Jersey Rank by Season', y=1.02)
plt.tight_layout()
plt.show()
