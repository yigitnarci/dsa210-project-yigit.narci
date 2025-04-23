import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1) Performans+trend tablolarını oku (önceden hazırladığın)
stats = pd.read_csv("nba_top8_comparison_num.csv", header=[0,1], index_col=0)
stats.index.name = "Season"
perf = stats.stack(level=1).reset_index().rename(columns={0:"Value"})
# elimizde multi-index; istersen GP/MIN/PPG olacak şekilde pivotla veya filtrele

# 2) Google trend ortalamaları
trend = pd.read_csv("combined_google_trends.csv", parse_dates=["date"])
trend_long = trend.melt(id_vars="date", var_name="Player", value_name="Trend")
# Sezonsal ortalama
season_ranges = {
  "2020-21":("2020-09-01","2021-08-31"),
  "2021-22":("2021-09-01","2022-08-31"),
  "2022-23":("2022-09-01","2023-08-31"),
  "2023-24":("2023-09-01","2024-08-31"),
  "2024-25":("2024-09-01","2025-04-30"),
}
trend_long["Season"] = None
for s,(st,ed) in season_ranges.items():
    mask = (trend_long.date>=st)&(trend_long.date<=ed)
    trend_long.loc[mask,"Season"] = s
trend_avg = (
    trend_long
    .dropna(subset=["Season"])
    .groupby(["Season","Player"], as_index=False)["Trend"]
    .mean()
)

# 3) Jersey rank tablosu
jersey = pd.read_csv("jersey_ranks.csv")  # yukarıdaki örnek CSV

# 4) Merge hepsi
df = (
    pd.merge(perf, trend_avg, on=["Season","Player"], how="inner")
      .merge(jersey, on=["Season","Player"], how="inner")
)

# 5) Artık df içinde şu sütunlar var:
#     Season, Player, level_1 (gym/min/ppg – eğer gerektiği gibi adlandırdıysan),
#     Value (o metriğin kendisi), Trend, JerseyRank

# 6) Scatter + annotation fonksiyonu
def plot_by_metric(metric_label):
    sub = df[df["level_1"] == metric_label]
    plt.figure(figsize=(8,5))
    sns.scatterplot(
        data=sub,
        x="JerseyRank",
        y="Value",
        hue="Season",
        style="Season",
        s=100,
        palette="tab10"
    )
    for _,row in sub.iterrows():
        plt.text(
            row.JerseyRank + 0.1,
            row.Value      + 0.1,
            row.Player,
            fontsize=7,
            alpha=0.8
        )
    plt.title(f"{metric_label} vs Jersey Rank")
    plt.xlabel("Jersey Rank")
    plt.ylabel(metric_label)
    plt.gca().invert_xaxis()  # istersen rank 1 en solda, 2 sonra vb.
    plt.legend(bbox_to_anchor=(1.02,1), title="Season")
    plt.tight_layout()
    plt.show()

# 7) Sırayla çizelim
for metric in ["Games Played","Minutes/Game","Points/Game","Trend"]:
    plot_by_metric(metric)
