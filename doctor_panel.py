import sqlite3
import os

# Database path
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "database", "clinsense.db")

def view_patients(doctor_name):
    """Doctor ला आजचे सर्व patients पाहता येतील"""
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    cur.execute('''SELECT name, symptoms, severity, appointment_time, waiting_time, status 
                   FROM patients 
                   WHERE doctor_assigned = ?''', (doctor_name,))
    
    data = cur.fetchall()
    conn.close()
    return data

# Example run
if __name__ == "__main__":
    doctor_name = "Dr. Mehta"
    patients = view_patients(doctor_name)
    if patients:
        print(f"Patients for {doctor_name}:")
        for p in patients:
            print(p)
    else:
        print(f"No patients assigned to {doctor_name}")
