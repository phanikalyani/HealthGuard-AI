from dd import get_db

def signup_user(name, email, password):
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password)
        )
        conn.commit()
        return True
    except:
        return False

def login_user(email, password):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, password)
    )
    return cur.fetchone()
