import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

# --- 1) Analiz edilecek oyuncular ve Basketball-Reference slug'ları ---
players = {
    "Luka Doncic":         "d/doncilu01",
    "Stephen Curry":       "c/curryst01",
    "LeBron James":        "j/jamesle01",
    "Jayson Tatum":        "t/tatumja01",
    "Jalen Brunson":       "b/brunsja01",
    "Victor Wembanyama":   "w/wembavi01",
    "Anthony Edwards":     "e/edwaran01",
    "Ja Morant":           "m/moranja01",
    "Giannis Antetokounmpo":"a/antetgi01",
    "Devin Booker":        "b/bookede01",
    "Kevin Durant":        "d/duranke01",
    "James Harden":        "h/hardeja01",
    "Joel Embiid":         "e/embiijo01",
    "Kyrie Irving":        "i/irvinky01",
}

base_url = "https://www.basketball-reference.com/players/"

all_data = []

for name, slug in players.items():
    url = f"{base_url}{slug}.html"
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    tbl = soup.find("table", id="per_game_stats")
    tbody = tbl.find("tbody")

    # 1) Tüm satırları (yıl, tr) olarak topla
    seasons = []
    for row in tbody.find_all("tr"):
        th = row.find("th", {"data-stat": "year_id"})
        if not th or not th.has_attr("csk"):
            continue
        year = int(th["csk"])
        seasons.append((year, row))

    # 2) En güncel 5 sezonu seç
    seasons = sorted(seasons, key=lambda yr_row: yr_row[0], reverse=True)[:5]

    # 3) Her sezonu işle
    for year, row in seasons:
        cols = row.find_all("td")
        gp  = cols[4].text.strip()      # games
        mpg = cols[6].text.strip()      # mp_per_g
        pts = cols[-2].text.strip()     # pts_per_g
        aw  = cols[-1].text.strip() or "No Awards"

        season_label = f"{year-1}-{str(year)[-2:]}"
        all_data.append({
            "Player": name,
            "Season": season_label,
            "Games Played": gp,
            "Minutes/Game": mpg,
            "Points/Game": pts,
            "Awards": aw
        })

    # siteye fazla yüklenmemek için kısa uyku
    sleep(1.0)

# 4) DataFrame oluştur ve CSV’ye kaydet
df = pd.DataFrame(all_data)
df = df.sort_values(["Player","Season"], ascending=[True,True])
df.to_csv("nba_top8_last5_by_player.csv", index=False)
print(df)
