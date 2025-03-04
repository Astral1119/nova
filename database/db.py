# database/db.py
import sqlite3
from pathlib import Path

# Use an absolute path to the database file
DB_PATH = Path("/home/lilac/discord-bot/database/sparkles.db")
print(f"Database path: {DB_PATH}")  # Debug statement

def init_db():
    """
    Initialize the database with the required tables.
    This function creates the 'sparkles' table if it doesn't already exist.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Create a table to store sparkle counts
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sparkles (
                user_id INTEGER PRIMARY KEY,
                epic INTEGER DEFAULT 0,
                rare INTEGER DEFAULT 0,
                regular INTEGER DEFAULT 0
            )
        """)
        conn.commit()

def update_sparkle(user_id: int, sparkle_type: str):
    """
    Update the sparkle count for a user.
    If the user doesn't exist in the database, they are added with a count of 1 for the specified sparkle type.
    If the user already exists, their count for the specified sparkle type is incremented by 1.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        # Insert or update the user's sparkle count
        cursor.execute(f"""
            INSERT INTO sparkles (user_id, {sparkle_type})
            VALUES (?, 1)
            ON CONFLICT(user_id) DO UPDATE SET
                {sparkle_type} = {sparkle_type} + 1
        """, (user_id,))
        conn.commit()

def get_leaderboard(sparkle_type: str, limit: int = 10):
    """
    Get the leaderboard for a specific sparkle type.
    Returns a list of tuples containing (user_id, sparkle_count) sorted in descending order.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT user_id, {sparkle_type}
            FROM sparkles
            ORDER BY {sparkle_type} DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()
