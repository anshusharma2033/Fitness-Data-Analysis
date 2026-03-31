import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users(
    name TEXT,
    email TEXT,
    password TEXT
)
''')
conn.commit()

def add_user(name, email, password):
    c.execute("INSERT INTO users VALUES (?, ?, ?)", (name, email, password))
    conn.commit()

def login_user(email, password):
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    return c.fetchone()