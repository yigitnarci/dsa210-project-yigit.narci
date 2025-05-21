# NBA Jersey Sales Analysis and Its Relationship with Player Performance and Popularity

## Project Proposal

This project will examine what influences NBA players' jersey sales. The goal is to understand how factors like **player performance and team achievements** contribute to jersey popularity.  
By analyzing these elements, I hope to figure out **which aspects most strongly relate to jersey sales and public interest** in NBA players.

### Research Questions:
- How does a player's **on-court performance** (points per game, games played, minutes played) affect jersey sales?
- Is there a relationship between **team success (e.g., championship, playoffs)** and jersey sales?
- Can **Google search trends** explain spikes in jersey sales?

---

## Data to be Used

The analysis is built on **multiple data sources**, focusing on **the top NBA jersey sales rankings** and enriched with player-specific variables.

| Data Source                                      | Data Collected                                      | Purpose                                         |
|--------------------------------------------------|-----------------------------------------------------|------------------------------------------------|
| **Hoopshype (Top Jersey Sales)**                 | Jersey sales rankings for each NBA season          | Main target variable (ranking of sales)       |
| **Basketball-Reference**                         | Points per Game (PTS), Games Played (GP), Total Minutes Played (MIN), Awards won (MVP, All-Star, etc.) | Player performance metrics                    |
| **Google Trends (via pytrends API)**             | Search trend index for player names               | Player public popularity/interest metric     |

---

## Data Collection Plan

The data was collected and **merged from multiple sources**:

### Step 1: **Primary Dataset (Jersey Sales)**
- Top-8 NBA jersey sales per season from Hoopshype.

### Step 2: **Performance & Popularity Metrics**
- Stats (PTS/Game, Games Played, Minutes Played, Award Count) from Basketball-Reference.
- Google Trends index collected via pytrends.

---

## Final Dataset Sample Structure:

| Player          | Season   | Jersey Rank | PTS/Game | Games Played | Minutes/Game | Award Count | Avg Google Trends |
|-----------------|----------|-------------|----------|----------------|----------------|---------------|--------------------|
| LeBron James    | 2022-23  | 1           | 25.7     | 71             | 35.3           | 3             | 21.5               |
| Stephen Curry   | 2024-25  | 2           | 26.1     | 73             | 34.9           | 0             | 20.2               |


---

# NBA Jersey Sales Analysis and Its Relationship with Player Performance and Popularity

## Project Overview
This project investigates the drivers of NBA jersey sales over five seasons by combining jersey sales rankings with player performance metrics, awards data, and Google search trends to uncover the most relevant predictors of popularity.

## Research Questions
- How does a player's **on-court performance** (points per game, games played, minutes per game) affect jersey sales?
- Does the **number of awards** influence player popularity through jersey sales?
- Can **Google search trends** explain jersey sales popularity?

---

## Data Sources
- **Jersey Sales** (`jersey_ranks.csv`): Top-8 jersey sales rank per season (1 = highest seller).
- **Performance & Awards** (`nba_top8_last5_cleaned_with_awards.csv`): Points/Game, Games Played, Minutes/Game, Award Count.
- **Google Trends** (`combined_google_trends.csv`): Weekly average search popularity scores for each player.

---

## Code Files Description

| File Name                        | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `stat_correlation.py`            | Calculates Spearman & Pearson correlations between jersey sales rank and player stats: Points/Game, Games Played, Minutes/Game, and Award Count. |
| `google_graph_correlation.py`    | Performs correlation analysis between Google Trends index and jersey sales rank, outputs both Spearman and Pearson values. |
| `pts_graph.py`                   | Generates scatter plot visualizing Points/Game by season and jersey rank. |
| `game_played_graph.py`           | Visualizes Games Played per season vs. jersey rank using color-coded year markers. |
| `minutepergame_played_graph.py` | Displays Minutes/Game data across five seasons and their relation to jersey ranks. |
| `award_graph.py`                 | Creates award count plots and analyzes their distribution with respect to jersey ranks. |
| `pearson_graph_hyp1.py`          | Generates Pearson regression plots for all stat-based metrics in one combined figure. |
| `google_graph.py`                | Creates a scatter plot of average Google Trends vs. jersey sales rank for all players. |
| `web scraping.py`                | Used for scraping season-by-season Google Trends data per player. (manual backup used in final version) |
| `combining_trend_stats.py`       | Merges cleaned jersey ranking data with Google Trends averages by season and player. |

---

## 📓 Notebook
You can view the project analysis notebook here: [🔗 dsa210_project_yigit_narci.ipynb](./dsa210_project_yigit_narci.ipynb)

## Exploratory Data Analysis (EDA)
Before running hypothesis tests, we visualized the data to explore trends across seasons and player profiles.

### Points per Game by Season
![PTS/Game by Year](figures/ptg-game-by-year.png)
Players with higher scoring averages do not consistently rank higher in jersey sales. This suggests that scoring alone may not be the main factor influencing fan purchases.

### Games Played by Season
![Games Played](figures/games-played-by-year.png)
There is no clear pattern between the number of games played and jersey rank. Some high-selling players missed several games, suggesting other factors may play a larger role.

### Minutes per Game by Season
![Minutes/Game](figures/minute-per-game-average-by-year.png)
Average playing time per game also shows no visible correlation with jersey sales rank. This further supports the notion that on-court activity is not the sole driver of popularity.

### Award Count by Season
![Award Count](figures/award-by-year.png)
Players with more awards are not always ranked higher in jersey sales. This could mean awards have limited impact unless paired with public visibility or media presence.

### Google Trends Index by Season
![Google Trends Index](figures/google-data-jersey-rank.png)

A noticeable trend shows that players with higher Google search popularity tend to have better jersey sales. This supports our second hypothesis regarding public interest.

---

## Hypotheses

### Hypothesis 1: Performance & Awards → Jersey Sales
- **H₀**: No correlation between PTS/Game, GP, MPG, Award Count and jersey rank.
- **H₁**: There is a correlation.

### Hypothesis 2: Google Trends → Jersey Sales
- **H₀**: No correlation between average Google Trends score and jersey rank.
- **H₁**: There is a correlation.

---

## Analytical Methods
- All datasets were cleaned and merged by `Season` and `Player`.
- **Statistical Tests**:
  - **Spearman & Pearson correlation** were calculated for all metrics using `stat_correlation.py`.
  - Google Trends correlations were computed with `google_graph_correlation.py`.

---

## Results

### Correlation Summary Table
| Metric         | Spearman ρ | p-value | Pearson r | p-value |
|----------------|-------------|---------|-----------|---------|
| Points/Game    |   0.095     |  0.586  |   0.089   |  0.614  |
| Games Played   |  -0.061     |  0.726  |  -0.053   |  0.752  |
| Minutes/Game   |  -0.068     |  0.700  |  -0.067   |  0.701  |
| Award Count    |  -0.149     |  0.393  |  -0.162   |  0.354  |
| Google Trends  |  -0.412     |  0.008  |  -0.374   |  0.017  |

### Interpretation

- **Performance & Awards**: No statistically significant correlation found for any metric.
  - H₀ retained.
- **Google Trends**: Strong, significant inverse correlation with jersey sales.
  - H₀ rejected, H₁ accepted.
  
We tested both hypotheses using Pearson and Spearman correlations, and found that while performance metrics such as points per game or award count had minimal influence, Google Trends data was a strong predictor of jersey sales. This indicates that popularity and public interest may outweigh pure athletic performance when it comes to fan purchasing behavior.

---


## Conclusion

- **Performance metrics and awards** do **not** significantly influence jersey sales rankings ⇒ H₀ retained.
- **Google search popularity** shows a statistically significant inverse correlation with jersey sales ⇒ H₀ rejected, H₁ accepted.

---

## Visualizations
Each visualization supports the respective hypothesis test, highlighting key trends across five seasons.

### 1. Stats-Based Hypothesis
- ![Pearson Full Stats](figures/pearson-fig-whole-stats.png)

### 2. Google Trends Hypothesis
- ![Pearson Google Index](figures/google-trend-pearson.png)

---

## GitHub Repository
[🔗 View Project on GitHub](https://github.com/yigitnarci/dsa210-project-yigit.narci)



