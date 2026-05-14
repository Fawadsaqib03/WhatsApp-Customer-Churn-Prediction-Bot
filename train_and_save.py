import os, joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

os.makedirs("artifacts", exist_ok=True)

# Load dataset
url = ("C:/Fawad's Data/Study Data/COMSATS/5th Semester/Business Application Using Machine Learning/Lab/Datasets/Churn_Modelling.csv")
df = pd.read_csv(url)

# Drop useless columns
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# Encode Geography and Gender (same as mid-project)
df = pd.get_dummies(df, columns=['Geography', 'Gender'], drop_first=True)

# Features and target
X = df.drop('Exited', axis=1)
y = df['Exited']

# Save feature names for reference
print("Feature order:", list(X.columns))

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)

# Scale
scaler = StandardScaler()
X_train_s = scaler.fit_transform(X_train)
X_test_s  = scaler.transform(X_test)

# Train Logistic Regression (same as mid-project)
model = LogisticRegression(C=0.5, max_iter=200)
model.fit(X_train_s, y_train)

print("Test accuracy:", model.score(X_test_s, y_test))

# Save
joblib.dump(model,  "artifacts/model.pkl")
joblib.dump(scaler, "artifacts/scaler.pkl")
print("Saved → artifacts/")