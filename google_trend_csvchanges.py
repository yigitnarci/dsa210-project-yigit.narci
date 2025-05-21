import pandas as pd

# 1. Veri setini yükle
df = pd.read_csv('combined_google_trends.csv')

# 2. Tarih sütununu datetime'a çevir
df['date'] = pd.to_datetime(df['date'])

# 3. Sezonları belirle (temmuz-haziran sezonları)
def get_season(date):
    year = date.year
    if date.month >= 7:  # Temmuz veya sonrası
        return f"{year}-{year + 1}"
    else:  # Ocak - Haziran
        return f"{year - 1}-{year}"

df['Season'] = df['date'].apply(get_season)

# 4. Wide to long: her oyuncu için tek sütun
df_long = df.melt(id_vars=['date', 'Season'], var_name='Player', value_name='Google Trends Score')

# 5. Sezon bazlı oyuncu ortalaması
df_season_avg = df_long.groupby(['Player', 'Season'])['Google Trends Score'].mean().reset_index()

# 6. CSV olarak kaydet (isteğe bağlı)
df_season_avg.to_csv('avg_google_trends_by_season.csv', index=False)

# 7. Kontrol
print(df_season_avg.head())
