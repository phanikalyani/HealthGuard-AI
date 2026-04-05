import streamlit as st
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

from db import *

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="HealthGuard AI", layout="centered")

st.title("🏥 HealthGuard AI")
st.subheader("Predicting Health Risks Before It’s Too Late")

st.markdown("""
*This tool provides an AI-based health risk estimate 
and is NOT a medical diagnosisimport streamlit as st * """)
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix

from db import *

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- SIDEBAR ----------------
if st.session_state.user:
    menu = ["Dashboard", "Contact", "Logout"]
else:
    menu = ["Login", "Sign Up"]

choice = st.sidebar.selectbox("Menu", menu)

# ---------------- SIGN UP ----------------
if choice == "Sign Up":
    st.subheader("📝 Create Account")

    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        if create_user(name, email, password):
            st.success("✅ Account created! Please login.")
        else:
            st.error("❌ Email already exists")

# ---------------- LOGIN ----------------
elif choice == "Login":
    st.subheader("🔐 Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        user = login_user(email, password)
        if user:
            st.session_state.user = user
            st.success("✅ Logged in successfully")
        else:
            st.error("❌ Invalid credentials")

# ---------------- DASHBOARD ----------------
elif choice == "Dashboard" and st.session_state.user:

    st.markdown("## 📊 HealthGuard Dashboard")
    st.write(f"Welcome, **{st.session_state.user[1]}** 👋")

    # -------- LOAD DATASET --------
    if os.path.exists("diabetes.csv"):

        data = pd.read_csv("diabetes.csv")
        st.success("✅ diabetes.csv Loaded Successfully")

        # Dataset Preview
        st.markdown("### 📄 Dataset Preview")
        st.dataframe(data.head())

        # Dataset Statistics
        st.markdown("### 📊 Dataset Statistics")
        st.write(data.describe())

        # -------- MODEL TRAINING --------
        X = data.drop("Outcome", axis=1)
        y = data["Outcome"]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        model = LogisticRegression()
        model.fit(X_train, y_train)

        st.success("🤖 AI Model Trained Successfully")

        # -------- MODEL ACCURACY --------
        accuracy = model.score(X_test, y_test)
        st.markdown("### 📈 Model Accuracy")
        st.success(f"Accuracy: {accuracy * 100:.2f}%")

        # -------- CONFUSION MATRIX --------
        st.markdown("### 📊 Confusion Matrix")

        y_pred = model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)

        fig, ax = plt.subplots()
        ax.imshow(cm)
        ax.set_xlabel("Predicted")
        ax.set_ylabel("Actual")
        ax.set_title("Confusion Matrix")

        for i in range(len(cm)):
            for j in range(len(cm)):
                ax.text(j, i, cm[i][j], ha="center", va="center")

        st.pyplot(fig)

        # -------- GLUCOSE DISTRIBUTION --------
        st.markdown("### 🧪 Glucose Distribution")

        fig2, ax2 = plt.subplots()
        ax2.hist(data["Glucose"], bins=20)
        ax2.set_title("Glucose Level Distribution")
        ax2.set_xlabel("Glucose")
        ax2.set_ylabel("Count")

        st.pyplot(fig2)

        # -------- BMI DISTRIBUTION --------
        st.markdown("### ⚖ BMI Distribution")

        fig3, ax3 = plt.subplots()
        ax3.hist(data["BMI"], bins=20)
        ax3.set_title("BMI Distribution")
        ax3.set_xlabel("BMI")
        ax3.set_ylabel("Count")

        st.pyplot(fig3)

        # -------- USER INPUT --------
        st.markdown("### 🧪 Enter Your Health Details")

        pregnancies = st.number_input("Pregnancies", 0, 20, 0)
        glucose = st.number_input("Glucose Level", 0, 300, 120)
        blood_pressure = st.number_input("Blood Pressure", 0, 200, 70)
        skin_thickness = st.number_input("Skin Thickness", 0, 100, 20)
        insulin = st.number_input("Insulin", 0, 900, 80)
        bmi = st.number_input("BMI", 0.0, 70.0, 25.0)
        diabetes_pedigree = st.number_input("Diabetes Pedigree Function", 0.0, 3.0, 0.5)
        age = st.number_input("Age", 1, 120, 30)

        # -------- PREDICTION --------
        if st.button("🔍 Predict Diabetes Risk"):

            user_data = np.array([[
                pregnancies, glucose, blood_pressure,
                skin_thickness, insulin, bmi,
                diabetes_pedigree, age
            ]])

            user_scaled = scaler.transform(user_data)
            prediction = model.predict(user_scaled)[0]
            probability = model.predict_proba(user_scaled)[0][1]

            if prediction == 1:
                st.error(f"⚠️ High Risk of Diabetes ({probability*100:.2f}%)")
            else:
                st.success(f"✅ Low Risk of Diabetes ({(1 - probability)*100:.2f}%)")

    else:
        st.error("❌ diabetes.csv not found in project folder.")
        st.stop()

# ---------------- CONTACT PAGE ----------------
elif choice == "Contact" and st.session_state.user:
    st.subheader("📩 Contact HealthGuard Team")

    message = st.text_area("Your Message")

    if st.button("Send Message"):
        add_feedback(st.session_state.user[2], message)
        st.success("✅ Message sent successfully!")

# ---------------- ADMIN PANEL ----------------
ADMIN_EMAIL = "admin@healthguard.ai"

if st.session_state.user and st.session_state.user[2] == ADMIN_EMAIL:
    st.markdown("## 👨‍💼 Admin Panel – User Feedback")

    feedbacks = get_all_feedback()
    if feedbacks:
        for f in feedbacks:
            st.write(f"📧 {f[1]} — {f[2]}")
    else:
        st.info("No feedback yet")

# ---------------- LOGOUT ----------------
if choice == "Logout":
    st.session_state.user = None
    st.success("Logged out successfully")
       
