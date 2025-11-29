import sqlite3
import os

# Database path
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "database", "clinsense.db")

def notify_patients(doctor_name):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute('''SELECT name, waiting_time FROM patients 
                   WHERE doctor_assigned=? AND status='Pending'
                   ORDER BY appointment_time''', (doctor_name,))
    patients = cur.fetchall()
    
    for name, wait in patients:
        if wait > 0:
            print(f"Patient Notification: '{name}', Your appointment will take place in {wait} minutes.")
            print(f"Doctor Notification: '{doctor_name}', Treatment will start in {wait}  minutes.")

    conn.close()

# Example run
if __name__ == "__main__":
    notify_patients("Dr. Mehta")
