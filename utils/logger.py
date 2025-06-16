import sqlite3
from datetime import datetime
import os

# Define log file and database path
LOG_FILE = "log.txt"
DB_FILE = "logs.db"

# Create the logs table if it doesn't exist
def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            prompt_version TEXT,
            duration REAL,
            message TEXT
        )
    """)
    conn.commit()
    conn.close()



def log_request(message, prompt_version, duration):
    # Automatically initialize DB if file does not exist
    if not os.path.exists(DB_FILE):
        init_db()
        
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Log to text file
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} | {prompt_version} | {duration:.2f}s | {message}\n")

    # Log to SQLite database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO logs (timestamp, prompt_version, duration, message)
        VALUES (?, ?, ?, ?)
    """, (timestamp, prompt_version, duration, message))
    conn.commit()
    conn.close()
