import streamlit as st
import pandas as pd
import numpy as np
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

from db import init_db, create_user, login_user

# ================= INIT =================
st.set_page_config(page_title="HealthGuard AI", layout="wide")
init_db()

# ================= PREMIUM UI =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #FDF6E3, #243B55);
    color: white;
}
h1, h2, h3 {
    color: #00C9A7;
}
.stButton>button {
    background-color: #00C9A7;
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
    return pd.DataFrame()

data = load_data()

# ================= MODEL =================
if not data.empty:
    X = data.drop("Outcome", axis=1)
    y = data["Outcome"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)
else:
    model = None

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= SIDEBAR =================
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Login", "Signup", "Dashboard", "Chatbot"]
)

# ================= HOME =================
if menu == "Home":
    st.title("🏥 HealthGuard AI")
    st.markdown("### 🚀 AI Health Prediction + Smart Doctor")
    st.info("⚠ This is not a medical diagnosis.")

# ================= SIGNUP =================
elif menu == "Signup":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if create_user(email, password):
            st.success("Account created")
        else:
            st.warning("User already exists")

# ================= LOGIN =================
elif menu == "Login":
    st.subheader("Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(email, password):
            st.session_state.user = email
            st.success("Login successful")
        else:
            st.error("Invalid credentials")

# ================= DASHBOARD =================
elif menu == "Dashboard":

    if st.session_state.user is None:
        st.warning("Login first")
        st.stop()

    st.subheader("📊 Health Prediction")

    pregnancies = st.number_input("Pregnancies", 0, 20)
    glucose = st.number_input("Glucose", 0, 200)
    bp = st.number_input("Blood Pressure", 0, 140)
    skin = st.number_input("Skin Thickness", 0, 100)
    insulin = st.number_input("Insulin", 0, 900)
    bmi = st.number_input("BMI", 0.0, 70.0)
    dpf = st.number_input("DPF", 0.0, 3.0)
    age = st.number_input("Age", 1, 120)

    if st.button("Predict"):
        if model is None:
            st.error("Dataset missing")
        else:
            input_data = np.array([[pregnancies, glucose, bp, skin, insulin, bmi, dpf, age]])
            pred = model.predict(input_data)[0]

            if pred == 1:
                st.error("⚠ High Risk of Diabetes")
            else:
                st.success("✅ Low Risk")
# ================= PRO MAX CHATBOT =================
elif menu == "Chatbot":

    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.subheader("🤖 AI Doctor Assistant (Pro Max)")

    # Chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # UI container
    chat_container = st.container()

    # Display chat history
    with chat_container:
        for role, msg in st.session_state.chat_history:
            if role == "user":
                st.markdown(f"🧑‍💻 **You:** {msg}")
            else:
                st.markdown(f"🤖 **Doctor AI:** {msg}")

    # Input
    user_input = st.text_input("Describe your symptoms...")

    # Quick buttons
    col1, col2, col3 = st.columns(3)
    if col1.button("🤒 Fever"):
        user_input = "fever"
    if col2.button("🤕 Headache"):
        user_input = "headache"
    if col3.button("🩸 Diabetes"):
        user_input = "diabetes"

    # Response engine
    def doctor_ai_response(text):
        text = text.lower()

        if "fever" in text:
            return "🌡️ You may have an infection. Stay hydrated, take rest, and monitor temperature."

        elif "diabetes" in text:
            return "🩸 Maintain a balanced diet, avoid sugar spikes, and check glucose regularly."

        elif "headache" in text:
            return "🤕 Could be stress or dehydration. Drink water, rest, and reduce screen time."

        elif "chest pain" in text:
            return "🚨 This could be serious. Please seek immediate medical attention!"

        elif "cough" in text:
            return "😷 Might be cold or allergy. Stay warm and drink fluids."

        else:
            return "⚕️ I'm here to help! Please describe your symptoms in more detail."

# ================= FOOTER =================
st.markdown("---")
st.markdown("Made with ❤️ | HealthGuard AI")
