import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

st.set_page_config(page_title="HealthGuard AI", layout="wide")

# ================= DATABASE =================
conn = sqlite3.connect("healthguard.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users(username TEXT, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS feedback(user TEXT, message TEXT)")
conn.commit()

# ================= LOAD DATA =================
@st.cache_data
def load_data():
    return pd.read_csv("diabetes.csv")

data = load_data()

# ================= TRAIN MODEL =================
X = data.drop("Outcome", axis=1)
y = data["Outcome"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier()
model.fit(X_train, y_train)

# ================= AUTH FUNCTIONS =================
def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone()

def create_user(username, password):
    c.execute("INSERT INTO users VALUES (?,?)", (username, password))
    conn.commit()

def add_feedback(user, message):
    c.execute("INSERT INTO feedback VALUES (?,?)", (user, message))
    conn.commit()

def get_all_feedback():
    c.execute("SELECT * FROM feedback")
    return c.fetchall()

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= SIDEBAR =================
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Login", "Signup", "Dashboard", "Feedback"]
)

# ================= HOME =================
if menu == "Home":
    st.title("🩺 HealthGuard AI")
    st.subheader("Predict health risks before it’s too late")

# ================= SIGNUP =================
elif menu == "Signup":

    st.subheader("Create Account")

    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")

    if st.button("Signup"):

        if new_user == "" or new_pass == "":
            st.warning("Please fill all fields")

        else:
            create_user(new_user, new_pass)
            st.success("Account created successfully")

# ================= LOGIN =================
elif menu == "Login":

    st.subheader("Login")

    user = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        result = login_user(user, password)

        if result:
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

    # ----------- CHARTS -----------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Diabetes Outcome Count")
        fig1, ax1 = plt.subplots()
        data["Outcome"].value_counts().plot(kind="bar", ax=ax1)
        st.pyplot(fig1)

    with col2:
        st.subheader("Outcome Distribution")
        fig2, ax2 = plt.subplots()
        data["Outcome"].value_counts().plot(kind="pie", autopct="%1.1f%%", ax=ax2)
        st.pyplot(fig2)

    st.subheader("Correlation Heatmap")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.heatmap(data.corr(), annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

    # ----------- USER INPUT -----------

    st.subheader("Enter Your Health Details")

    pregnancies = st.number_input("Pregnancies", 0, 20)
    glucose = st.number_input("Glucose", 0, 200)
    blood_pressure = st.number_input("Blood Pressure", 0, 140)
    skin_thickness = st.number_input("Skin Thickness", 0, 100)
    insulin = st.number_input("Insulin", 0, 900)
    bmi = st.number_input("BMI", 0.0, 70.0)
    dpf = st.number_input("Diabetes Pedigree Function", 0.0, 3.0)
    age = st.number_input("Age", 1, 120)

    input_data = np.array([[pregnancies, glucose, blood_pressure,
                            skin_thickness, insulin, bmi, dpf, age]])

    if st.button("Predict"):

        prediction = model.predict(input_data)[0]

        input_df = pd.DataFrame(input_data, columns=X.columns)

        st.subheader("Your Input Data")
        st.dataframe(input_df)

        if prediction == 1:
            st.error("⚠ High Risk of Diabetes")
        else:
            st.success("✅ Low Risk of Diabetes")

# ================= FEEDBACK =================
elif menu == "Feedback":

    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.subheader("Send Feedback")

    msg = st.text_area("Your message")

    if st.button("Submit Feedback"):
        add_feedback(st.session_state.user, msg)
        st.success("Feedback submitted")

    st.subheader("All Feedback")

    for row in get_all_feedback():
        st.write(f"👤 {row[0]} ➜ {row[1]}")
