import sqlite3

# Connect to database
connection = sqlite3.connect("finance.db")

# Create cursor
cursor = connection.cursor()


# Create Users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")


# Create Transactions table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    type TEXT NOT NULL,
    source TEXT,
    category TEXT,
    amount REAL NOT NULL,
    date TEXT NOT NULL,
    FOREIGN KEY(user_email) REFERENCES users(email)
)
""")


# Save changes
connection.commit()


print("Database connected successfully!")
