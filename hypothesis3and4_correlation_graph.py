import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr

# 1. Load the enriched dataset with BMI
df = pd.read_csv('full_enriched_dataset_with_bmi.csv')

# 2. Prepare data, drop missing values
df_len = df[['length', 'Jersey Rank']].dropna()
df_bmi = df[['BMI', 'Jersey Rank']].dropna()

# 3. Compute Pearson correlations
r_len, p_len = pearsonr(df_len['length'], df_len['Jersey Rank'])
r_bmi, p_bmi = pearsonr(df_bmi['BMI'], df_bmi['Jersey Rank'])

# 4. Create side-by-side Pearson scatter plots with regression lines
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Length vs. Jersey Rank
axes[0].scatter(df_len['length'], df_len['Jersey Rank'])
m1, b1 = np.polyfit(df_len['length'], df_len['Jersey Rank'], 1)
x1 = np.array([df_len['length'].min(), df_len['length'].max()])
axes[0].plot(x1, m1 * x1 + b1)
axes[0].set_title(f'Length vs. Jersey Rank\nPearson r={r_len:.2f}, p={p_len:.3f}')
axes[0].set_xlabel('Length (cm)')
axes[0].set_ylabel('Jersey Rank (1 = top seller)')

# Plot 2: BMI vs. Jersey Rank
axes[1].scatter(df_bmi['BMI'], df_bmi['Jersey Rank'])
m2, b2 = np.polyfit(df_bmi['BMI'], df_bmi['Jersey Rank'], 1)
x2 = np.array([df_bmi['BMI'].min(), df_bmi['BMI'].max()])
axes[1].plot(x2, m2 * x2 + b2)
axes[1].set_title(f'BMI vs. Jersey Rank\nPearson r={r_bmi:.2f}, p={p_bmi:.3f}')
axes[1].set_xlabel('BMI')
axes[1].set_ylabel('Jersey Rank (1 = top seller)')

plt.tight_layout()
plt.show()
