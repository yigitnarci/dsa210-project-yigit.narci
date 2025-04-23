import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

# 1) Load & clean
jersey = pd.read_csv('jersey_ranks.csv')  
stats  = pd.read_csv('nba_top8_last5_cleaned_with_awards.csv')

for df in (jersey, stats):
    df.columns   = df.columns.str.strip()
    df['Season'] = df['Season'].astype(str).str.strip()
    df['Player'] = df['Player'].astype(str).str.strip()

# unify seasons
def unify(s):
    s = s.replace('–','-')
    a = s.split('-')
    return f"{a[0]}-{a[1][2:]}" if len(a)==2 and len(a[0])==4 and len(a[1])==4 else s

jersey['Season'] = jersey['Season'].apply(unify)
stats ['Season'] = stats ['Season'].apply(unify)

# ensure Award Count column
if 'Awards' in stats.columns:
    stats = stats.rename(columns={'Awards':'Award Count'})
stats['Award Count'] = pd.to_numeric(stats['Award Count'], errors='coerce').fillna(0)

# merge
df = pd.merge(
    jersey[['Season','Player','Rank']],
    stats [['Season','Player','Points/Game','Games Played','Minutes/Game','Award Count']],
    on=['Season','Player'],
    how='inner'
).dropna(subset=['Rank'])

df['Rank'] = df['Rank'].astype(int)

# 2) Plotting function
def pearson_scatter(x, y, ax):
    # scatter + regression
    sns.regplot(x=x, y=y, data=df, ax=ax, scatter_kws={'s':60}, line_kws={'color':'C1'})
    # compute Pearson
    r, p = pearsonr(df[x].dropna(), df[y].dropna())
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"r = {r:.2f}, p = {p:.3f}")
    # invert rank axis so 1 is top
    if y=='Rank':
        ax.invert_yaxis()

# 3) Make figure with 4 subplots: each metric vs Rank
metrics = ['Points/Game','Games Played','Minutes/Game','Award Count']
fig, axes = plt.subplots(2, 2, figsize=(12,10), sharey=True)
axes = axes.flatten()

for ax, m in zip(axes, metrics):
    pearson_scatter(m, 'Rank', ax)

fig.suptitle("Pearson Scatter + Regression vs Jersey Rank", fontsize=16, y=0.95)
plt.tight_layout()
plt.show()
