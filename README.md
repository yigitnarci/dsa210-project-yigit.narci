# NBA Jersey Sales Analysis and Its Relationship with Player Performance and Popularity

## Project Proposal

This project will examine what influences NBA players' jersey sales. The goal is to understand how factors like **player performance, social media presence, and team achievements** contribute to jersey popularity.  
By analyzing these elements, I hope to figure out **which aspects most strongly relate to jersey sales and public interest** in NBA players.

### Research Questions:
- How does a player's **on-court performance** (points per game, games played, minutes played) affect jersey sales?
- How important is **social media popularity (e.g., Instagram followers)** in determining jersey sales?
- Is there a relationship between **team success (e.g., championship, playoffs)** and jersey sales?
- Can **Google search trends** explain spikes in jersey sales?

---

## Data to be Used

The analysis will be built on **multiple data sources**, focusing on **the top NBA jersey sales rankings** and enriched with player-specific and team-specific variables.

| Data Source                                      | Data Collected                                      | Purpose                                         |
|--------------------------------------------------|-----------------------------------------------------|------------------------------------------------|
| **Hoopshype (Top Jersey Sales)**                 | Jersey sales rankings for each NBA season          | Main target variable (ranking of sales)       |
| **Basketball-Reference**                         | Points per Game (PTS), Games Played (GP), Total Minutes Played (MIN), Awards won (MVP, All-Star, etc.) | Player performance metrics                    |
| **Instrack / SocialBlade / Manual**              | Instagram follower counts                          | Player social media popularity indicator     |
| **Google Trends (via pytrends API)**             | Search trend index for player names               | Player public popularity/interest metric     |
| **NBA.com / Basketball-Reference (Teams)**      | Team success: Champion status (0/1), Playoff status (0/1) | To analyze team effect on jersey sales       |

---

## Data Collection Plan

I plan to collect and **merge the following data** to create a dataset:

### Step 1: **Primary Dataset (Jersey Sales)**
- **Top NBA jersey sales lists** from Hoopshype for the past several seasons.
- Each season's **top 20 players** ranked by jersey sales.

### Step 2: **Enrichment Variables**
| Variable                                     | Collection Method                                       |
|----------------------------------------------|------------------------------------------------------|
| **Points per Game (PTS)**                    | Web scraping from **Basketball-Reference** (Python) |
| **Games Played (GP)**                        | Web scraping from **Basketball-Reference** (Python) |
| **Total Minutes Played (MIN)**               | Web scraping from **Basketball-Reference** (Python) |
| **Awards Won (All-Star, MVP, DPOY)**          | Web scraping from **Basketball-Reference**, player career highlights |
| **Instagram Followers (M)**                   | Manual collection for top players (or using Instrack/SocialBlade when available) |
| **Google Trends Index**                      | Automated collection via **pytrends API** (Python)    |
| **Team Champion (0/1)**                      | Manual or semi-automated from NBA.com and Basketball-Reference |
| **Team Playoff (0/1)**                       | Manual or semi-automated from NBA.com and Basketball-Reference |

---

### Step 3: **Data Enrichment and Final Dataset Creation**
- All datasets will be merged using **player name** and **season/year**.
- **Final dataset columns** will include:
  - `Player Name`
  - `Season`
  - `Jersey Rank` (based on sales)
  - `PTS (Per Game)`
  - `GP (Games Played)`
  - `MIN (Total Minutes Played)`
  - `Awards Won`
  - `Instagram Followers (Millions)`
  - `Google Trends Index`
  - `Champion (0/1)`
  - `Playoff (0/1)`

---

### Example of Final Dataset Structure:

| Player          | Jersey Rank | PTS (Per Game) | GP | MIN | Instagram (M) | Google Trends Index | Champion (0/1) | Playoff (0/1) |
|-----------------|-------------|----------------|----|-----|---------------|---------------------|----------------|---------------|
| Stephen Curry   | 2           | 26             | 64 | 2100| 55            | 70                  | 0              | 1             |
| LeBron James    | 1           | 25             | 55 | 1900| 150           | 85                  | 0              | 1             |
| Luka Doncic     | 3           | 28             | 70 | 2400| 8             | 55                  | 0              | 0             |

---

## Final Notes
- This project will involve **data scraping, data cleaning, and merging from multiple sources**, ensuring a rich dataset for analysis.
- The analysis will combine **player performance, social trends, and team factors**, giving a comprehensive view of what drives NBA jersey sales.
- The project will be **regularly updated on GitHub**, with code, data, and analysis results being shared.
