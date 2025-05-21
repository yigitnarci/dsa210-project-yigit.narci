import pandas as pd
from scipy.stats import pearsonr, spearmanr

# Load the enriched dataset with BMI
df = pd.read_csv('full_enriched_dataset_with_bmi.csv')

# Drop rows with missing values in relevant columns
df_length = df[['length', 'Jersey Rank']].dropna()
df_bmi = df[['BMI', 'Jersey Rank']].dropna()

# 1. Correlation tests for length vs. Jersey Rank
pearson_len_r, pearson_len_p = pearsonr(df_length['length'], df_length['Jersey Rank'])
spearman_len_rho, spearman_len_p = spearmanr(df_length['length'], df_length['Jersey Rank'])

# 2. Correlation tests for BMI vs. Jersey Rank
pearson_bmi_r, pearson_bmi_p = pearsonr(df_bmi['BMI'], df_bmi['Jersey Rank'])
spearman_bmi_rho, spearman_bmi_p = spearmanr(df_bmi['BMI'], df_bmi['Jersey Rank'])

# Display results
print("Length vs. Jersey Rank")
print(f"  Pearson ρ = {pearson_len_r:.3f}, p-value = {pearson_len_p:.3f}")
print(f"  Spearman ρ = {spearman_len_rho:.3f}, p-value = {spearman_len_p:.3f}\n")

print("BMI vs. Jersey Rank")
print(f"  Pearson ρ = {pearson_bmi_r:.3f}, p-value = {pearson_bmi_p:.3f}")
print(f"  Spearman ρ = {spearman_bmi_rho:.3f}, p-value = {spearman_bmi_p:.3f}")
