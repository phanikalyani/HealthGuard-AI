import streamlit as st
import pandas as pd
import numpy as np
import os

from db import init_db, create_user, login_user

# ================= INIT =================
st.set_page_config(page_title="HealthGuard AI", layout="wide")
init_db()

# ================= UI STYLE =================
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #141E30, #243B55);
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

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None

# ================= SIDEBAR =================
menu = st.sidebar.selectbox("Navigation", ["Home", "Login", "Signup", "Chatbot"])

# ================= HOME =================
if menu == "Home":
    st.title("🏥 HealthGuard AI")
    st.markdown("### 🚀 AI Health Risk Prediction & Smart Doctor Assistant")
    st.info("⚠ This tool provides AI insights, not a medical diagnosis.")

# ================= SIGNUP =================
elif menu == "Signup":
    st.subheader("Create Account")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if create_user(email, password):
            st.success("Account created successfully")
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

# ================= CHATBOT =================
elif menu == "Chatbot":

    if st.session_state.user is None:
        st.warning("Please login first")
        st.stop()

    st.subheader("🤖 AI Doctor Assistant")

    user_input = st.text_input("Describe your symptoms...")

    if st.button("Get Advice"):

        if "fever" in user_input.lower():
            st.info("You may have an infection. Stay hydrated and consult a doctor.")

        elif "diabetes" in user_input.lower():
            st.info("Maintain healthy diet, monitor sugar levels regularly.")

        elif "headache" in user_input.lower():
            st.info("Take rest, hydrate, reduce screen time.")

        else:
            st.info("Please consult a healthcare professional for accurate diagnosis.")
