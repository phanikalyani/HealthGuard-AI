import sqlite3

def get_connection():
    return sqlite3.connect("healthguard.db", check_same_thread=False)

# ================= INIT DB =================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
    """)

    # FEEDBACK TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        user TEXT,
        message TEXT
    )
    """)

    # HISTORY TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        user TEXT,
        glucose REAL,
        bmi REAL,
        age INTEGER,
        result INTEGER
    )
    """)

    conn.commit()
    conn.close()

# ================= AUTH =================
def create_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    try:
        c.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (username, password)
        )
        conn.commit()
    except:
        pass

    conn.close()

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username, password)
    )

    result = c.fetchone()
    conn.close()

    return result

# ================= HISTORY =================
def save_history(user, glucose, bmi, age, result):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        INSERT INTO history (user, glucose, bmi, age, result)
        VALUES (?, ?, ?, ?, ?)
    """, (user, glucose, bmi, age, result))

    conn.commit()
    conn.close()

def get_history(user):
    import pandas as pd

    conn = get_connection()
    df = pd.read_sql_query(
        "SELECT * FROM history WHERE user=?",
        conn,
        params=(user,)
    )
    conn.close()
    return df

# ================= FEEDBACK =================
def add_feedback(user, message):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        "INSERT INTO feedback (user, message) VALUES (?, ?)",
        (user, message)
    )

    conn.commit()
    conn.close()

def get_feedback():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM feedback")
    data = c.fetchall()

    conn.close()
    return data

