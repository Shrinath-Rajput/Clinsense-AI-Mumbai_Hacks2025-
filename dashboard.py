import streamlit as st
import sqlite3
import os

# ✅ FIXED IMPORT
from frontend.templates.auth import is_logged_in

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "clinic.db")


# ---------------- DB LOAD ---------------- #
def load_all_appointments():
    if not os.path.exists(DB_PATH):
        return []

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("""
            SELECT id, username, patient_name, age,
                   specialization, doctor_name,
                   date, time, symptoms, created_at
            FROM appointments
            ORDER BY date DESC, time DESC
        """)
        return cur.fetchall()


# ---------------- MAIN UI ---------------- #
def show_dashboard():
    st.subheader("👨‍⚕️ Doctor Dashboard")

    # 🔐 Admin check
    if not st.session_state.get("is_admin", False):
        st.error("🚫 Admin Login Required")
        return

    data = load_all_appointments()

    if not data:
        st.info("No appointments yet.")
        return

    st.success(f"Total Appointments: {len(data)}")

    for row in data:
        (
            appt_id,
            username,
            patient_name,
            age,
            specialization,
            doctor_name,
            date,
            time,
            symptoms,
            created_at,
        ) = row

        header = f"#{appt_id} - {patient_name} ({specialization})"

        with st.expander(header):
            st.write(f"👤 Patient: {patient_name}")
            st.write(f"👨 Username: {username}")
            st.write(f"🎂 Age: {age}")
            st.write(f"🩺 Specialization: {specialization}")
            st.write(f"👨‍⚕️ Doctor: {doctor_name}")
            st.write(f"📅 Date: {date}")
            st.write(f"⏰ Time: {time}")
            st.write(f"📝 Symptoms: {symptoms}")
            st.caption(f"Created: {created_at}")