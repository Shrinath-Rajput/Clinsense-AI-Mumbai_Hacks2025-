import sqlite3

# CONNECT TO DATABASE
conn = sqlite3.connect("database/clinsense.db")
cur = conn.cursor()

# DOCTOR ENTRIES (PERFECT, NO SYNTAX ERROR)
doctors = [
    ("Dr. Aakash", "Fever"),
    ("Dr. Sneha", "Headache"),
    ("Dr. Patil", "Diabetes"),
    ("Dr. Kiran", "Heart Problem"),
    ("Dr. Neha", "Cold & Cough"),
    ("Dr. Raju", "Stomach Pain"),
    ("Dr. Maya", "Skin Infection"),
    ("Dr. Joshi", "Asthma"),
    ("Dr. Mehta", "Cancer"),
    ("Dr. Rohit", "BP High"),
    ("Dr. Priya", "BP Low"),
    ("Dr. Sunil", "Allergy"),
    ("Dr. Kavita", "Kidney Issue"),
    ("Dr. Gaurav", "Liver Issue"),
    ("Dr. Ishika", "Eye Issue"),
    ("Dr. Tejal", "Sugar")     # ← HERE comma is present!
]

# INSERT DATA
cur.executemany("INSERT INTO doctors (name, speciality) VALUES (?, ?)", doctors)

conn.commit()
conn.close()

print("✔ Doctors added successfully!")
