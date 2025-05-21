import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

# 1. Load data
df = pd.read_csv('full_enriched_dataset_with_bmi.csv')

# 2. Create sales_tier target
bins = [0, 3, 6, 8]
labels = ['High', 'Mid', 'Low']
df['sales_tier'] = pd.cut(df['Jersey Rank'], bins=bins, labels=labels)

# 3. Select features and drop any rows with NA
features = ['Points/Game','Games Played','Minutes/Game','Award Count',
            'Google Trends Score','length','BMI']
data = df[features + ['sales_tier']].dropna()
X = data[features]
y = data['sales_tier']

# 4. Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y)

# 5. Train Random Forest
clf = RandomForestClassifier(random_state=42)
clf.fit(X_train, y_train)

# 6. Predict & evaluate
y_pred = clf.predict(X_test)
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))

# 7. Feature importances
importances = clf.feature_importances_
plt.figure(figsize=(6,4))
plt.barh(features, importances)
plt.title("Feature Importances")
plt.xlabel("Importance")
plt.show()
