import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# --- 1) Load & clean your CSVs ---
jersey = pd.read_csv('jersey_ranks.csv')  
stats  = pd.read_csv('nba_top8_last5_cleaned_with_awards.csv')

for df in (jersey, stats):
    df.columns    = df.columns.str.strip()
    df['Season']  = df['Season'].astype(str).str.strip()
    df['Player']  = df['Player'].astype(str).str.strip()

def unify_season(s):
    s = s.replace('–','-')
    a = s.split('-')
    if len(a)==2 and len(a[0])==4 and len(a[1])==4:
        return f"{a[0]}-{a[1][2:]}"
    return s

jersey['Season'] = jersey['Season'].apply(unify_season)
stats ['Season'] = stats ['Season'].apply(unify_season)

# ensure the award‐column is named “Award Count”
if 'Awards' in stats.columns:
    stats = stats.rename(columns={'Awards':'Award Count'})

df = (
    pd.merge(
        jersey[['Season','Player','Rank']],
        stats [['Season','Player','Award Count']],
        on=['Season','Player'],
        how='left'
    )
    .dropna(subset=['Award Count'])
)

df['Rank']        = df['Rank'].astype(int)
df['Award Count'] = df['Award Count'].astype(int)   # make sure it's int

# --- 2) Build a FacetGrid (5 panels) ---
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

g.map_dataframe(
    sns.scatterplot,
    x='Award Count',
    y='Rank',
    hue='Season',
    palette='tab10',
    s=80,
    legend=False
)

# annotate & force integer x‐ticks
for ax, (season, subdf) in zip(g.axes.flat, df.groupby('Season')):
    ax.invert_yaxis()
    # integer ticks only
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    for _, row in subdf.iterrows():
        ax.text(row['Award Count'], row['Rank'], row['Player'],
                fontsize=8, va='center', ha='left')

    for lbl in ax.get_xticklabels():
        lbl.set_rotation(45)
        lbl.set_horizontalalignment('right')

g.set_axis_labels('Award Count', 'Jersey Rank (1 = top seller)')
g.fig.suptitle('Award Count vs. Jersey Rank by Season', y=1.02)
plt.tight_layout()
plt.show()
