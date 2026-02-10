import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
# Load dataset
data = pd.read_csv("diabetes.csv")
# Replace zero values with median (medical relevance)
cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in cols_with_zero:
data[col] = data[col].replace(0, data[col].median())
# Features and target
X = data.drop('Outcome', axis=1)
y = data['Outcome']
# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
X, y, test_size=0.2, random_state=42
)
# Feature scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)
# Model training
model = LogisticRegression()
model.fit(X_train, y_train)
# Evaluation
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy * 100:.2f}%")
# Sample prediction (example user input)
# Order: Pregnancies, Glucose, BP, SkinThickness, Insulin, BMI, DPF, Age
sample_user = np.array([[2, 140, 80, 25, 100, 28.5, 0.5, 35]])
sample_user = scaler.transform(sample_user)
risk_probability = model.predict_proba(sample_user)[0][1]
print(f"Diabetes Risk Probability: {risk_probability * 100:.2f}%")
