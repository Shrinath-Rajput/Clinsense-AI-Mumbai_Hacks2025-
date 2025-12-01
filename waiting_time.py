import sqlite3
import os

# Database path
base_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(base_dir, "..", "database", "clinsense.db")

def update_waiting_time(doctor_name, busy_minutes):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Update doctor status
    cur.execute('''UPDATE doctors 
                   SET status='Busy', next_available_time=datetime('now', '+' || ? || ' minutes')
                   WHERE name=?''', (busy_minutes, doctor_name))

    # Pending patients
    cur.execute('''SELECT patient_id, appointment_time 
                   FROM patients 
                   WHERE doctor_assigned=? AND status='Pending'
                   ORDER BY appointment_time''', (doctor_name,))
    patients = cur.fetchall()

    for i, (pid, app_time) in enumerate(patients):
        new_wait = busy_minutes + i*15  # 15 min per patient
        cur.execute('''UPDATE patients SET waiting_time=? WHERE patient_id=?''', (new_wait, pid))
    
    conn.commit()
    conn.close()
    print(f"Waiting time updated for patients of {doctor_name}")

# Example run
if __name__ == "__main__":
    update_waiting_time("Dr. Mehta", 30)
