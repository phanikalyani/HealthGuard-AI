import streamlit as st

# MUST BE FIRST
st.set_page_config(page_title="HealthGuard AI", layout="wide")

# other imports
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt # pyright: ignore[reportMissingModuleSource]
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from db import *

# NOW safe
init_db()
# ================= CONFIG =================
st.set_page_config(page_title="HealthGuard AI", layout="wide")
init_db()

# ================= UI STYLE =================
st.markdown("""
<style>
body {
    background: linear-gradient(to right, #667eea, #764ba2);
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    if os.path.exists("diabetes.csv"):
        return pd.read_csv("diabetes.csv")
    else:
        return pd.DataFrame()

data = load_data()

# ================= MODEL =================
if not data.empty:
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= MENU =================
menu = st.sidebar.selectbox("Navigation",
      ["Home", "Login", "Signup", "Dashboard", "Feedback"]
)

# ================= HOME =================
if menu == "Home":
    st.title("🩺 HealthGuard AI")
    st.caption("AI-powered early disease prediction & smart health assistant")

    st.info("Login or Signup to start predicting your health risk")

# ================= SIGNUP =================
elif menu == "Signup":
    st.subheader("📝 Create Account")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Signup"):
        if create_user(user, pw):
            st.success("Account created successfully ✅")
        else:
            st.warning("User already exists")

# ================= LOGIN =================
elif menu == "Login":
    st.subheader("🔐 Login")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(user, pw):
            st.session_state.user = user
            st.session_state.pw=pw
            st.success("Login successful ✅")
        else:
            st.error("Invalid credentials ❌")

# ================= DASHBOARD =================
elif menu == "Dashboard":

    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.title("📊 Health Dashboard")

    if data.empty:
        st.error("Dataset not found")
        st.stop()

    st.subheader("Dataset Preview")
    st.dataframe(data.head())

    # ----------- CHARTS -----------
    col1, col2 = st.columns(2)

    with col1:
        fig1, ax1 = plt.subplots()
        data["Outcome"].value_counts().plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

    with col2:
        fig2, ax2 = plt.subplots()
        data["Outcome"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        st.pyplot(fig2)

    st.subheader("Correlation Heatmap")
    fig3, ax3 = plt.subplots()
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

    # ----------- INPUT -----------
    st.subheader("🧾 Enter Health Details")

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

    # ----------- HISTORY -----------
    st.subheader("📈 Your History")

    hist = get_history(st.session_state.user)

    if not hist.empty:
        st.line_chart(hist[["glucose", "bmi"]])
    else:
        st.info("No history available")

    # ----------- AI ASSISTANT -----------
    st.subheader("🤖 AI Assistant")

    q = st.text_input("Ask about health")

    if q:
        q = q.lower()
        if "diet" in q:
            st.write("🥗 Eat healthy, low sugar foods")
        elif "exercise" in q:
            st.write("🏃 Exercise daily")
        else:
            st.write("💡 Maintain healthy lifestyle")

# ================= FEEDBACK =================
elif menu == "Feedback":

    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.subheader("💬 Feedback")

    msg = st.text_area("Your message")

    if st.button("Submit"):
        add_feedback(st.session_state.user, msg)
        st.success("Feedback submitted")

    for f in get_feedback():
        st.write(f"👤 {f[0]} ➜ {f[1]}")

# ================= LOGOUT =================
st.sidebar.markdown("---")
if  st.sidebar.button("Logout"):
    st.session_state.user = None
    st.success("Logged out successfully")
