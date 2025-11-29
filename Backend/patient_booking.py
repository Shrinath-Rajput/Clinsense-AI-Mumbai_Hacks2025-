import sqlite3
import os
from datetime import datetime, timedelta

# Database path
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "database", "clinsense.db")

# Function: Add new patient booking
def add_patient(name, symptoms, severity):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Get available doctor (first one with status 'Available')
    cur.execute("SELECT doctor_id, name FROM doctors WHERE status='Available' LIMIT 1")
    doctor = cur.fetchone()

    if doctor:
        doctor_id, doctor_name = doctor
    else:
        doctor_id, doctor_name = None, "No Doctor Available"

    # Calculate appointment time and waiting time
    appointment_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    waiting_time = 0  # default

    cur.execute('''INSERT INTO patients 
        (name, symptoms, severity, doctor_assigned, appointment_time, waiting_time, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)''',
        (name, symptoms, severity, doctor_name, appointment_time, waiting_time, "Pending")
    )

    conn.commit()
    conn.close()
    print(f"✅ Patient '{name}' booked with Doctor: {doctor_name}")

# Example run
if __name__ == "__main__":
    add_patient("Rohit Patil", "Fever, Cough", "Medium")
