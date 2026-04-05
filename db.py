import sqlite3
import bcrypt
import pandas as pd

# ✅ Safe connection (no global lock)
def get_connection():
    return sqlite3.connect("healthguard.db", timeout=10)

# ================= INIT DB =================
def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        username TEXT PRIMARY KEY,
        password BLOB,
        age INTEGER,
        weight REAL,
        height REAL
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        user TEXT,
        glucose REAL,
        bmi REAL,
        age INTEGER,
        prediction INTEGER
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS feedback(
        user TEXT,
        message TEXT
    )
    """)

    conn.commit()
    conn.close()

# ================= USER =================
def create_user(username, password, age, weight, height):
    conn = get_connection()
    c = conn.cursor()

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    try:
        c.execute("INSERT INTO users VALUES (?,?,?,?,?)",
                  (username, hashed, age, weight, height))
        conn.commit()
    except:
        return False

    conn.close()
    return True

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
def save_history(user, glucose, bmi, age, prediction):
    conn = get_connection()
    c = conn.cursor()

    c.execute()
    c.execute("INSERT INTO history VALUES (?,?,?,?,?)",
              (user, glucose, bmi, age, prediction))

    conn.commit()
    conn.close()
def get_history(user):
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM history WHERE user=?",
        conn,
        params=(user,)
    )
    conn.close()
    return df
    
    def add_feedback(user, msg):
        conn = get_connection()
    c = conn.cursor()

    c.execute("INSERT INTO feedback VALUES (?,?)", (user, msg))

    conn.commit()
    conn.close()


def get_feedback():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT * FROM feedback")
    data = c.fetchall()

    conn.close()
    return data
