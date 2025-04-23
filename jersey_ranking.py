import pandas as pd

# 1) Sezon bazlı sıralamalarını bir dict içinde tanımlıyoruz
jersey_data = {
    '2024-2025': [
        'Luka Doncic',
        'Stephen Curry',
        'LeBron James',
        'Jayson Tatum',
        'Jalen Brunson',
        'Victor Wembanyama',
        'Anthony Edwards',
        'Ja Morant'
    ],
    '2023-2024': [
        'Stephen Curry',
        'Jayson Tatum',
        'LeBron James',
        'Victor Wembanyama',
        'Giannis Antetokounmpo',
        'Luka Doncic',
        'Devin Booker',
        'Kevin Durant'
    ],
    '2022-2023': [
        'LeBron James',
        'Stephen Curry',
        'Jayson Tatum',
        'Giannis Antetokounmpo',
        'Luka Doncic',
        'Kevin Durant',
        'Devin Booker',
        'Ja Morant'
    ],
    '2021-2022': [
        'LeBron James',
        'James Harden',
        'Stephen Curry',
        'Kevin Durant',
        'Jayson Tatum',
        'Joel Embiid',
        'Giannis Antetokounmpo',
        'Luka Doncic'
    ],
    '2020-2021': [
        'LeBron James',
        'Giannis Antetokounmpo',
        'Kevin Durant',
        'Luka Doncic',
        'Jayson Tatum',
        'Devin Booker',
        'Stephen Curry',
        'Kyrie Irving'
    ]
}

# 2) satır satır açıp 'Season', 'Rank', 'Player' sütunları olarak listeye ekliyoruz
rows = []
for season, players in jersey_data.items():
    for rank, player in enumerate(players, start=1):
        rows.append({
            'Season': season,
            'Rank': rank,
            'Player': player
        })

# 3) DataFrame'e dönüştür ve CSV'ye yaz
df = pd.DataFrame(rows)
df.to_csv('jersey_ranks.csv', index=False)

print("Oluşan CSV'nin ilk 10 satırı:")
print(df.head(10))
