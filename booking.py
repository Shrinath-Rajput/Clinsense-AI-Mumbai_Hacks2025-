import streamlit as st
import sqlite3
import os
from datetime import datetime, time as dt_time

# ✅ FIXED IMPORT
from frontend.templates.auth import is_logged_in

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "clinic.db")

# --------------------- DOCTOR DATA --------------------- #
DOCTORS = {
    "General Physician": [
        {"name": "Dr. Arjun Patil", "status": "available", "delay_min": 0, "available_on": None, "slots": ["09:30", "10:00"]},
        {"name": "Dr. Meera Joshi", "status": "busy", "delay_min": 10, "available_on": None, "slots": ["09:00", "12:00"]},
    ]
}

# --------------------- DB INIT --------------------- #
def init_booking_table():
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                patient_name TEXT,
                age INTEGER,
                specialization TEXT,
                doctor_name TEXT,
                symptoms TEXT,
                date TEXT,
                time TEXT,
                created_at TEXT
            )
        """)
        conn.commit()


def save_appointment(username, patient_name, age,
                     specialization, doctor_name,
                     symptoms, date, time_):
    init_booking_table()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            INSERT INTO appointments
            (username, patient_name, age, specialization, doctor_name,
             symptoms, date, time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, patient_name, age, specialization,
            doctor_name, symptoms, date, time_,
            datetime.now().isoformat()
        ))
        conn.commit()


# --------------------- MAIN UI --------------------- #
def show_booking():
    init_booking_table()
    st.subheader("📅 Patient Booking")

    if not is_logged_in():
        st.warning("🔐 Please login to book appointment")
        return

    username = st.session_state.get("user", "guest")

    patient_name = st.text_input("Patient Name")
    age = st.number_input("Age", 0, 120, 25)
    specialization = st.selectbox("Specialization", list(DOCTORS.keys()))
    symptoms = st.text_area("Symptoms")
    date = st.date_input("Date")
    time_ = st.time_input("Time")

    doctor = DOCTORS[specialization][0]

    if st.button("Book Appointment"):
        if not patient_name:
            st.error("Enter patient name")
            return

        save_appointment(
            username,
            patient_name,
            age,
            specialization,
            doctor["name"],
            symptoms,
            str(date),
            time_.strftime("%H:%M")
        )

        st.success(f"✅ Appointment booked with {doctor['name']}")
