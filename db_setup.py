import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "clinsense.db")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    speciality TEXT,
    status TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    symptoms TEXT,
    doctor_assigned TEXT,
    appointment_time TEXT,
    status TEXT
)
""")

doctors = [
    ("Dr. Pooja", "Fever", "Available"),
    ("Dr. Ramesh", "Sugar", "Available"),
    ("Dr. Vishal", "Cancer", "Available"),
    ("Dr. Mansi", "Skin Infection", "Available"),
    ("Dr. Rohan", "BP High", "Available"),
]

cur.executemany("INSERT INTO doctors (name, speciality, status) VALUES (?, ?, ?)", doctors)
conn.commit()
conn.close()

print("✅ Database created successfully!")
