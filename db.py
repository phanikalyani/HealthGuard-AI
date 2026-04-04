import sqlite3
import hashlib

# Connect to SQLite database (auto-creates if it doesn't exist)
conn = sqlite3.connect("healthguard.db", check_same_thread=False)
c = conn.cursor()

# ---------------- CREATE TABLES ----------------

# Users table
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

# Feedback table
c.execute("""
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    message TEXT NOT NULL
)
""")

conn.commit()

# ---------------- PASSWORD HASHING ----------------

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ---------------- USER FUNCTIONS ----------------

def create_user(name, email, password):
    try:
        hashed_password = hash_password(password)
        c.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False


def login_user(email, password):
    hashed_password = hash_password(password)
    c.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hashed_password)
    )
    return c.fetchone()


# ---------------- FEEDBACK FUNCTIONS ----------------

def add_feedback(email, message):
    c.execute(
        "INSERT INTO feedback (user_email, message) VALUES (?, ?)",
        (email, message)
    )
    conn.commit()


def get_all_feedback():
    c.execute("SELECT * FROM feedback")
    return c.fetchall()


