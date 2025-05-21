import pandas as pd

# 1. Ham all_seasons.csv dosyasını yükle
df = pd.read_csv('all_seasons.csv')

# 2. İlgili oyuncu listesini tanımla
players = [
    'Luka Doncic', 'Stephen Curry', 'LeBron James', 'Jayson Tatum',
    'Jalen Brunson', 'Shai Gilgeous-Alexander', 'Nikola Jokić',
    'Giannis Antetokounmpo', 'Victor Wembanyama', 'Devin Booker',
    'Kevin Durant', 'Ja Morant', 'James Harden', 'Joel Embiid',
    'Kyrie Irving'
]

# 3. Filtrele ve aynı oyuncunun sadece ilk kaydını tut
df_filtered = (
    df[df['player_name'].isin(players)]
    .drop_duplicates(subset='player_name', keep='first')
)

# 4. Victor Wembanyama eksikse elle ekle
if 'Victor Wembanyama' not in df_filtered['player_name'].values:
    victor = {
        'player_name': 'Victor Wembanyama',
        'player_height': 221.0,
        'player_weight': 107.0
    }
    # Diğer sütunları NaN ile doldur
    for col in df_filtered.columns:
        victor.setdefault(col, pd.NA)
    df_filtered = pd.concat([df_filtered, pd.DataFrame([victor])], ignore_index=True)

# 5. Sadece gerekli üç sütunu seç
df_final = df_filtered[['player_name', 'player_height', 'player_weight']]

# 6. Son CSV'yi kaydet
df_final.to_csv('final_players.csv', index=False)

# 7. Kontrol amaçlı ekrana bas (opsiyonel)
print(df_final)
