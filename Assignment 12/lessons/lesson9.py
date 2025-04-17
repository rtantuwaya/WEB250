import sqlite3


def initialize():
    init_db()

# Database helper function
def get_db_connection():
    conn = sqlite3.connect('records.db')  # Ensure you're using the correct database file
    conn.row_factory = sqlite3.Row  # Makes rows return as dictionaries
    return conn

# Create the database and table (only need to run this once)
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            age INTEGER,
            created_at DATE
        )
    ''')
    conn.commit()
    conn.close()


# Get all records from the database

def get_records():
    conn = get_db_connection()
    records = conn.execute('SELECT * FROM records').fetchall()  # Get all records from the database
    conn.close()
    return records
