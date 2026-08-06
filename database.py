import sqlite3
from config import DATABASE_NAME, OWNER_ID

def get_connection():
    return sqlite3.connect(DATABASE_NAME)

def init_database():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        status TEXT DEFAULT 'started',
        verify_time TEXT,
        join_time TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS admins(
        user_id INTEGER PRIMARY KEY,
        role TEXT DEFAULT 'owner'
    )
    """)

    cur.execute("""
    INSERT OR IGNORE INTO admins(user_id, role)
    VALUES(?, 'owner')
    """, (OWNER_ID,))

    conn.commit()
    conn.close()
