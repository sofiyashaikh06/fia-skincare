import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Product table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    skin_type TEXT,
    concern TEXT,
    category TEXT
)
""")

# Orders table  ← ADD THIS
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT,
    phone TEXT,
    address TEXT,
    payment TEXT,
    total INTEGER
)
""")

conn.commit()
conn.close()

print("Database and tables created successfully.")