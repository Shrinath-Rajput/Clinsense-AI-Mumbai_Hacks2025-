import sqlite3
import os

base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "database", "clinsense.db")

def add_doctor(name, speciality, status="Available"):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute('''INSERT INTO doctors (name, speciality, status, next_available_time)
                   VALUES (?, ?, ?, ?)''',
                (name, speciality, status, None))
    conn.commit()
    conn.close()
    print(f"✅ Doctor '{name}' added successfully.")

# Example run
if __name__ == "__main__":
    add_doctor("Dr. Mehta", "Cardiologist")
    add_doctor("Dr. Sharma", "General")
