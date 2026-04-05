import sqlite3
import bcrypt

# ================= CONNECTION =================
def get_connection():
    return sqlite3.connect("healthguard.db", check_same_thread=False)

# ================= INIT DB =================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password BLOB
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history (
        user TEXT,
        glucose REAL,
        bmi REAL,
        age INTEGER,
        result INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        user TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

# ================= AUTH =================
def create_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                  (username, hashed))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT password FROM users WHERE username=?", (username,))
    result = c.fetchone()
    conn.close()

    if result:
        return bcrypt.checkpw(password.encode(), result[0])
    return False

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

    c.execute("INSERT INTO feedback VALUES (?, ?)", (user, message))

    conn.commit()
    conn.close()

def get_feedback():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM feedback")
    data = c.fetchall()

    conn.close()
    return data
