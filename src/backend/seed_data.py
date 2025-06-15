import sqlite3

conn = sqlite3.connect("customers.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    gender TEXT NOT NULL,
    location TEXT NOT NULL
)''')

cursor.executemany("INSERT INTO customers (name, gender, location) VALUES (?, ?, ?)", [
    ("Alice", "Female", "Mumbai"),
    ("Bob", "Male", "Delhi"),
    ("Clara", "Female", "Mumbai"),
    ("Dan", "Male", "Kolkata"),
    ("Eva", "Female", "Chennai"),
    ("Frank", "Male", "Bangalore"),
    ("Grace", "Female", "Delhi"),
    ("Hank", "Transgender", "Mumbai"),
    ("Ivy", "Female", "Bangalore"),
    ("Jack", "Male", "Delhi"),
    ("Kathy", "Female", "Mumbai"),
    ("Leo", "Male", "Hyderabad"),
    ("Mia", "Transgender", "Kolkata"),
    ("Nina", "Female", "Jammu and Kashmir"),
    ("Oscar", "Male", "Delhi"),
    ("Paul", "Male", "Hyderabad"),
    ("Quinn", "Female", "Hyderabad"),
    ("Rita", "Female", "Assam"),
    ("Sam", "Male", "Delhi"),
    ("Tina", "Transgender", "Mumbai"),
    ("Uma", "Female", "Hyderabad"),
    ("Vikram", "Male", "Delhi"),
    ("Wendy", "Transgender", "Pune"),
    ("Xander", "Transgender", "Pune"),
    ("Yara", "Female", "Goa"),
    ("Zara", "Female", "Hyderabad"),
    ("Aaron", "Male", "Bangalore"),
    ("Bella", "Transgender", "Assam"),
    ("Charlie", "Transgender", "Jammu and Kashmir"),
    ("Diana", "Transgender", "Delhi"),
    ("Ethan", "Male", "Bangalore"),
])

conn.commit()
conn.close()