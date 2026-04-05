from db import init_db, login_user, create_user, save_history, get_history, add_feedback, get_feedback
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from db import *
from utils import calculate_bmi

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# ================= CONFIG =================
st.set_page_config(page_title="HealthGuard AI", layout="wide")

# ================= INIT =================
if "initialized" not in st.session_state:
    init_db()
    st.session_state.initialized = True

if "user" not in st.session_state:
    st.session_state.user = None

# ================= UI STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#141e30,#243b55);
    color:white;
}
h1,h2,h3 { color:#00f5ff; }
.stButton>button {
    background: linear-gradient(45deg,#00f5ff,#00c6ff);
    color:lightgray;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOGO =================
st.markdown("""
<div style="display:flex;align-items:center;gap:10px;">
<img src="https://cdn-icons-png.flaticon.com/512/2966/2966489.png" width="50">
<h1>HealthGuard AI</h1>

</div>
<hr>
""", unsafe_allow_html=True)

# ================= LOAD / TRAIN MODEL =================
@st.cache_data
def load_data():
    if os.path.exists("diabetes.csv"):
        return pd.read_csv("diabetes.csv")
    else:
        return pd.DataFrame({
            "Pregnancies":[1,2,3,4],
            "Glucose":[85,120,150,130],
            "BloodPressure":[66,70,80,75],
            "SkinThickness":[29,30,32,28],
            "Insulin":[0,100,130,90],
            "BMI":[26.6,28.1,30.5,27.2],
            "DiabetesPedigreeFunction":[0.351,0.672,0.8,0.5],
            "Age":[31,45,50,40],
            "Outcome":[0,1,1,0]
        })

data = load_data()

X = data.drop("Outcome", axis=1)
y = data["Outcome"]

model = RandomForestClassifier()
model.fit(X, y)

# ================= SIDEBAR =================
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Login", "Signup", "Dashboard", "Feedback"]
)

def add_feedback(user, msg):
    raise NotImplementedError

# ================= HOME =================
if menu == "Home":
    st.title("🛡 AI Healthcare Platform")
    st.write("Predict diseases early and stay healthy.")

# ================= SIGNUP =================
elif menu == "Signup":
    st.subheader("Create Account")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")
    age = st.number_input("Age", 1, 120)
    weight = st.number_input("Weight (kg)")
    height = st.number_input("Height (cm)")

    if st.button("Signup"):
        if create_user(user, pw, age, weight, height):
            st.success("Account created")
        else:
            st.error("User already exists")

# ================= LOGIN =================
elif menu == "Login":
    st.subheader("Login")

    user = st.text_input("username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(user, pw):
            st.session_state.user = user
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ================= DASHBOARD =================
elif menu == "Dashboard":

    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.title("📊 Health Dashboard")

    st.subheader("Dataset Preview")
    st.dataframe(data)

    # ================= CHARTS =================
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Outcome Count")
        fig1, ax1 = plt.subplots()
        data["Outcome"].value_counts().plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("Outcome Distribution")
        fig2, ax2 = plt.subplots()
        data["Outcome"].value_counts().plot(
            kind="pie", autopct="%1.1f%%", ax=ax2
        )
        st.pyplot(fig2)

    st.subheader("Correlation Heatmap")
    fig3, ax3 = plt.subplots(figsize=(10,6))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

    # ================= USER INPUT =================
    st.subheader("Enter Health Details")

    pregnancies = st.number_input("Pregnancies", 0, 20)
    glucose = st.number_input("Glucose", 0, 200)
    bp = st.number_input("Blood Pressure", 0, 140)
    skin = st.number_input("Skin Thickness", 0, 100)
    insulin = st.number_input("Insulin", 0, 900)
    bmi_input = st.number_input("BMI", 0.0, 70.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0)
    age = st.number_input("Age", 1, 120)

    input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi_input, dpf, age]])

    if st.button("Predict"):

        pred = model.predict(input_data)[0]
        prob = model.predict_proba(input_data)[0][1]

        st.metric("Risk Score", f"{prob*100:.2f}%")

        if pred == 1:
            st.error("⚠ High Risk of Diabetes")
        else:
            st.success("✅ Low Risk")

        # Save history
        save_history(st.session_state.user, glucose, bmi_input, age, int(pred))

        # Show input
        # Show input data
        input_df = pd.DataFrame(input_data, columns=X.columns)
        st.subheader("Your Input Data")
        st.dataframe(input_df)

        # ================= SMART ALERTS =================
        st.subheader("🚨 Health Alerts")

        if glucose > 140:
            st.warning("High glucose level detected!")

        if bmi_input > 30:
            st.warning("Obesity risk detected!")

        if age > 45:
            st.info("Regular health checkups recommended")

        # ================= DOWNLOAD REPORT =================
        report = f"""
Health Report

User: {st.session_state.user}
Glucose: {glucose}
BMI: {bmi_input}
Age: {age}

Risk Score: {prob*100:.2f}%
Prediction: {"High Risk" if pred==1 else "Low Risk"}
"""
        st.download_button("📄 Download Report", report, file_name="report.txt")

    # ================= HISTORY =================
    st.subheader("📈 Your Health History")

    hist = get_history(st.session_state.user)

    if not hist.empty:
        st.line_chart(hist["glucose"])
    else:
        st.info("No history available yet")

    # ================= AI ASSISTANT =================
    st.subheader("🤖 Health Assistant")

    query = st.text_input("Ask something...")

    if query:
        q = query.lower()

        if "diet" in q:
            st.write("🥗 Eat low sugar, high fiber foods")

        elif "exercise" in q:
            st.write("🏃 Do 30 mins cardio daily")

        elif "diabetes" in q:
            st.write("⚠ Monitor glucose regularly")

        else:
            st.write("💡 Maintain healthy lifestyle")

# ================= FEEDBACK =================
elif menu == "Feedback":

    
    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.subheader("💬 Send Feedback")

    msg = st.text_area("Your feedback")

    if st.button("Submit Feedback"):
        add_feedback(st.session_state.user, msg)
        st.success("Feedback submitted successfully!")

    st.subheader("📜 All Feedback")

    feedbacks = get_feedback()

    if feedbacks:
        for row in feedbacks:
            st.write(f"👤 {row[0]} ➜ {row[1]}")
    else:
        st.info("No feedback yet")

# ================= LOGOUT =================
st.sidebar.markdown("---")
if st.sidebar.button("Logout"):
    st.session_state.user = None
    st.success("Logged out successfully")
