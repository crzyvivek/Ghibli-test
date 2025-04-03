# database.py - Database Management File

import sqlite3

# Database initialization
conn = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = conn.cursor()

# Create Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    photos_used INTEGER DEFAULT 0,
    plan TEXT DEFAULT NULL
)
""")

# Create Transactions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    plan TEXT,
    amount INTEGER,
    status TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
)
""")

conn.commit()

# Function to add new user
def add_user(user_id, username):
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
    conn.commit()

# Function to get user details
def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

# Function to update user plan
def update_plan(user_id, plan):
    cursor.execute("UPDATE users SET plan=?, photos_used=0 WHERE user_id=?", (plan, user_id))
    conn.commit()

# Function to update photo count
def update_photo_usage(user_id):
    cursor.execute("UPDATE users SET photos_used = photos_used + 1 WHERE user_id=?", (user_id,))
    conn.commit()

# Function to check photo limit
def check_photo_limit(user_id, plan):
    cursor.execute("SELECT photos_used FROM users WHERE user_id=?", (user_id,))
    photos_used = cursor.fetchone()[0] if cursor.fetchone() else 0
    return photos_used < plan

# Function to add a transaction
def add_transaction(user_id, plan, amount, status="Pending"):
    cursor.execute("INSERT INTO transactions (user_id, plan, amount, status) VALUES (?, ?, ?, ?)",
                   (user_id, plan, amount, status))
    conn.commit()

# Function to update transaction status
def update_transaction_status(transaction_id, status):
    cursor.execute("UPDATE transactions SET status=? WHERE transaction_id=?", (status, transaction_id))
    conn.commit()
