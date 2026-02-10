import streamlit as st
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("diabetes.csv")

# Replace zero values
cols_with_zero = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
for col in cols_with_zero:
    data[col] = data[col].replace(0, data[col].median())

X = data.drop('Outcome', axis=1)
y = data['Outcome']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
# Train model
model = LogisticRegression()
model.fit(X_scaled, y)

# UI
st.set_page_config(page_title="HealthGuard AI", layout="centered")
st.title("🩺 HealthGuard AI")
st.subheader("Predicting Health Risks Before It’s Too Late")
st.markdown("⚠️ This tool provides an AI-based risk estimate and is not a medical diagnosis.")


# Inputs
preg = st.number_input("Pregnancies", 0, 20, 1)
glucose = st.slider("Glucose Level", 50, 200, 120)
bp = st.slider("Blood Pressure", 40, 140, 80)
skin = st.slider("Skin Thickness", 5, 100, 25)
insulin = st.slider("Insulin Level", 15, 300, 100)
bmi = st.slider("BMI", 10.0, 50.0, 25.0)
dpf = st.slider("Diabetes Pedigree Function", 0.0, 2.5, 0.5)
age = st.slider("Age", 10, 90, 30)

if st.button("🔍 Predict Risk"):
    user_data = np.array([[preg, glucose, bp, skin, insulin, bmi, dpf, age]])
    user_scaled = scaler.transform(user_data)
    risk = model.predict_proba(user_scaled)[0][1]

    st.success(f"Diabetes Risk Probability: {risk * 100:.2f}%")

    if risk > 0.6:
        st.warning("High risk detected. Consider consulting a healthcare professional.")
    else:
        st.info("Low risk detected. Maintain a healthy lifestyle.")
