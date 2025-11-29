# frontend/templates/booking.py

import streamlit as st
import sqlite3
import os
from datetime import datetime, time as dt_time

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "clinic.db")

# --------------------- DOCTOR DATA --------------------- #
# इथे तुला हवे असलेले डॉक्टर add / edit करू शकतोस
# प्रत्येक doctor कडे:
# name, status (available / busy / unavailable), delay_min, available_on, slots (["HH:MM", ...])
DOCTORS = {
    "General Physician": [
        {
            "name": "Dr. Arjun Patil",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "10:00", "11:00", "13:00", "15:00"],
        },
        {
            "name": "Dr. Meera Joshi",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["09:00", "12:00", "14:30"],
        },
        {
            "name": "Dr. Rajesh Sharma",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-01",
            "slots": [],
        },
    ],

    "Pediatrician": [
        {
            "name": "Dr. Nidhi Kulkarni",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "11:30", "16:00"],
        },
        {
            "name": "Dr. Sameer Pawar",
            "status": "busy",
            "delay_min": 15,
            "available_on": None,
            "slots": ["09:00", "10:30", "14:00"],
        },
        {
            "name": "Dr. Pooja Khatri",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-28",
            "slots": [],
        },
    ],

    "Dermatologist": [
        {
            "name": "Dr. Priya Dhawale",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "10:00", "11:00"],
        },
        {
            "name": "Dr. Riya Mehta",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["12:00", "14:00", "16:00"],
        },
        {
            "name": "Dr. Saurabh Kothari",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["10:30", "13:00", "17:00"],
        },
    ],

    "Cardiologist": [
        {
            "name": "Dr. Manish Kumar",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:00", "14:00"],
        },
        {
            "name": "Dr. Pooja Pandey",
            "status": "busy",
            "delay_min": 20,
            "available_on": None,
            "slots": ["10:30", "13:30", "16:00"],
        },
        {
            "name": "Dr. Viraj Soni",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-05",
            "slots": [],
        },
    ],

    "Neurologist": [
        {
            "name": "Dr. Neha Kulkarni",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["11:00", "11:30", "12:00", "12:30"],
        },
        {
            "name": "Dr. Amit Pawar",
            "status": "busy",
            "delay_min": 15,
            "available_on": None,
            "slots": ["10:00", "10:30", "11:00"],
        },
        {
            "name": "Dr. Shubham Rathod",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-29",
            "slots": [],
        },
    ],

    "Psychiatrist": [
        {
            "name": "Dr. Anuja Desai",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "11:00", "15:00"],
        },
        {
            "name": "Dr. Karan Jadhav",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["10:00", "12:30", "17:00"],
        },
        {
            "name": "Dr. Rohan Shetty",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-10",
            "slots": [],
        },
    ],

    "Orthopedic Surgeon": [
        {
            "name": "Dr. Shashank Patankar",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "12:00", "16:00"],
        },
        {
            "name": "Dr. Prajakta More",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["09:30", "11:30", "14:30"],
        },
        {
            "name": "Dr. Umesh Giri",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-02",
            "slots": [],
        },
    ],

    "ENT Specialist": [
        {
            "name": "Dr. Nikhil Sane",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "10:30", "12:00"],
        },
        {
            "name": "Dr. Jyoti Kharat",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["11:00", "13:00", "16:00"],
        },
        {
            "name": "Dr. Mayur Dange",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-27",
            "slots": [],
        },
    ],

    "Ophthalmologist": [
        {
            "name": "Dr. Snehal Patil",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "11:00", "14:00"],
        },
        {
            "name": "Dr. Chetan Bhosale",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["10:00", "12:30", "16:30"],
        },
        {
            "name": "Dr. Shruti Rao",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-03",
            "slots": [],
        },
    ],

    "Dentist": [
        {
            "name": "Dr. Kunal Thakur",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "11:30", "15:00"],
        },
        {
            "name": "Dr. Roshni Jain",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["09:00", "13:00", "17:00"],
        },
        {
            "name": "Dr. Harshita Goyal",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-30",
            "slots": [],
        },
    ],

    "Pulmonologist": [
        {
            "name": "Dr. Sagar Naik",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:00", "14:00"],
        },
        {
            "name": "Dr. Anjali Tiwari",
            "status": "busy",
            "delay_min": 20,
            "available_on": None,
            "slots": ["10:30", "13:00", "16:00"],
        },
        {
            "name": "Dr. Imran Shaikh",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-08",
            "slots": [],
        },
    ],

    "Gastroenterologist": [
        {
            "name": "Dr. Mohit Agrawal",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "11:30", "15:00"],
        },
        {
            "name": "Dr. Shraddha Soni",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["10:00", "13:00", "16:30"],
        },
        {
            "name": "Dr. Ajinkya Patil",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-05",
            "slots": [],
        },
    ],

    "Endocrinologist": [
        {
            "name": "Dr. Pranav Kulkarni",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "12:00", "15:00"],
        },
        {
            "name": "Dr. Vaishnavi Deshpande",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["09:30", "11:30", "14:30"],
        },
        {
            "name": "Dr. Ravi Nair",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-29",
            "slots": [],
        },
    ],

    "Gynecologist": [
        {
            "name": "Dr. Smita Kulshreshtha",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:00", "13:00", "16:00"],
        },
        {
            "name": "Dr. Poonam Wagh",
            "status": "busy",
            "delay_min": 15,
            "available_on": None,
            "slots": ["10:30", "12:30", "17:00"],
        },
        {
            "name": "Dr. Rachana Jagtap",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-04",
            "slots": [],
        },
    ],

    "Oncologist": [
        {
            "name": "Dr. Vivek Iyer",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "11:30", "15:00"],
        },
        {
            "name": "Dr. Manasi Gokhale",
            "status": "busy",
            "delay_min": 20,
            "available_on": None,
            "slots": ["09:00", "13:00", "16:30"],
        },
        {
            "name": "Dr. Aditya Chauhan",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-10",
            "slots": [],
        },
    ],

    "Nephrologist": [
        {
            "name": "Dr. Rahul Bhat",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "11:00", "14:00"],
        },
        {
            "name": "Dr. Nisha Fernandes",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["10:30", "13:00", "17:00"],
        },
        {
            "name": "Dr. Kiran Shastri",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-30",
            "slots": [],
        },
    ],

    "Urologist": [
        {
            "name": "Dr. Sandeep More",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "12:00", "16:00"],
        },
        {
            "name": "Dr. Tanvi Shah",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["09:30", "11:30", "15:00"],
        },
        {
            "name": "Dr. Imtiaz Khan",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-06",
            "slots": [],
        },
    ],

    "Rheumatologist": [
        {
            "name": "Dr. Shweta Bajaj",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:30", "14:30"],
        },
        {
            "name": "Dr. Harish Menon",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["10:00", "13:00", "16:00"],
        },
        {
            "name": "Dr. Aparna Kulkarni",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-01",
            "slots": [],
        },
    ],

    "Hematologist": [
        {
            "name": "Dr. Rehan Siddiqui",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "12:00", "15:00"],
        },
        {
            "name": "Dr. Kavya Narayan",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["09:30", "11:30", "16:00"],
        },
        {
            "name": "Dr. Lokesh Patnaik",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-09",
            "slots": [],
        },
    ],

    "Neonatologist": [
        {
            "name": "Dr. Rutuja Sawant",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:00", "14:00"],
        },
        {
            "name": "Dr. Krishnaraj Reddy",
            "status": "busy",
            "delay_min": 15,
            "available_on": None,
            "slots": ["10:30", "13:00", "16:00"],
        },
        {
            "name": "Dr. Bhavana Naik",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-29",
            "slots": [],
        },
    ],

    "Physiotherapist": [
        {
            "name": "Dr. Yogesh More",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "11:00", "15:00"],
        },
        {
            "name": "Dr. Anushka Jain",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["10:00", "12:30", "17:00"],
        },
        {
            "name": "Dr. Swapnil Gaikwad",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-02",
            "slots": [],
        },
    ],

    "Dietician / Nutritionist": [
        {
            "name": "Dt. Namrata Shah",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:00", "14:00"],
        },
        {
            "name": "Dt. Rohit Koli",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["10:30", "13:00", "16:00"],
        },
        {
            "name": "Dt. Sneha Jaiswal",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-07",
            "slots": [],
        },
    ],

    "Diabetologist": [
        {
            "name": "Dr. Sanjay Jha",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "12:00", "15:00"],
        },
        {
            "name": "Dr. Payal Bhatt",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["09:30", "11:30", "16:30"],
        },
        {
            "name": "Dr. Aman Khanna",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-30",
            "slots": [],
        },
    ],

    "Surgeon (General)": [
        {
            "name": "Dr. Ajay Suryavanshi",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:30", "15:00"],
        },
        {
            "name": "Dr. Madhuri Patankar",
            "status": "busy",
            "delay_min": 20,
            "available_on": None,
            "slots": ["10:30", "13:00", "17:00"],
        },
        {
            "name": "Dr. Omkar Chitale",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-03",
            "slots": [],
        },
    ],

    "Plastic Surgeon": [
        {
            "name": "Dr. Aniket Kulkarni",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["10:00", "12:00", "16:00"],
        },
        {
            "name": "Dr. Janhavi Shelar",
            "status": "busy",
            "delay_min": 15,
            "available_on": None,
            "slots": ["09:30", "11:30", "15:30"],
        },
        {
            "name": "Dr. Tarun Mehra",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-08",
            "slots": [],
        },
    ],

    "Radiologist": [
        {
            "name": "Dr. Shripad Naidu",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "10:30", "13:00", "16:00"],
        },
        {
            "name": "Dr. Neelima Rane",
            "status": "busy",
            "delay_min": 5,
            "available_on": None,
            "slots": ["11:00", "14:00", "17:00"],
        },
        {
            "name": "Dr. Danish Khan",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-01",
            "slots": [],
        },
    ],

    "Pathologist": [
        {
            "name": "Dr. Seema Dogra",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:30", "11:30", "14:30"],
        },
        {
            "name": "Dr. Yash Patil",
            "status": "busy",
            "delay_min": 10,
            "available_on": None,
            "slots": ["10:00", "13:00", "16:00"],
        },
        {
            "name": "Dr. Nivedita Rao",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-11-28",
            "slots": [],
        },
    ],

    "Anesthesiologist": [
        {
            "name": "Dr. Gaurav Malhotra",
            "status": "available",
            "delay_min": 0,
            "available_on": None,
            "slots": ["09:00", "11:00", "15:00"],
        },
        {
            "name": "Dr. Ishita Paul",
            "status": "busy",
            "delay_min": 15,
            "available_on": None,
            "slots": ["10:30", "13:30", "17:00"],
        },
        {
            "name": "Dr. Nitin Raval",
            "status": "unavailable",
            "delay_min": 0,
            "available_on": "2025-12-02",
            "slots": [],
        },
    ],
}

# --------------------- DB INIT --------------------- #
def init_booking_table():
    os.makedirs(DB_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
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
            """
        )
        cols = [c[1] for c in conn.execute("PRAGMA table_info(appointments)")]
        if "doctor_name" not in cols:
            conn.execute("ALTER TABLE appointments ADD COLUMN doctor_name TEXT;")
        conn.commit()


def save_appointment(username, patient_name, age,
                     specialization, doctor_name,
                     symptoms, date, time_):
    init_booking_table()
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            INSERT INTO appointments
            (username, patient_name, age, specialization, doctor_name,
             symptoms, date, time, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                username,
                patient_name,
                age,
                specialization,
                doctor_name,
                symptoms,
                date,
                time_,
                datetime.now().isoformat(),
            ),
        )
        conn.commit()


def load_appointments(username=None):
    init_booking_table()
    with sqlite3.connect(DB_PATH) as conn:
        if username:
            cur = conn.execute(
                """
                SELECT id, patient_name, age, specialization, doctor_name,
                       date, time, symptoms, created_at
                FROM appointments
                WHERE username = ?
                ORDER BY date DESC, time DESC
                """,
                (username,),
            )
        else:
            cur = conn.execute(
                """
                SELECT id, patient_name, age, specialization, doctor_name,
                       date, time, symptoms, created_at
                FROM appointments
                ORDER BY date DESC, time DESC
                """
            )
        rows = cur.fetchall()
    return rows


# --------------------- HELPERS --------------------- #
def time_to_str(t: dt_time) -> str:
    return t.strftime("%H:%M")


def format_doctor_label(doc: dict) -> str:
    """Dropdown मध्ये doctor label कसं दिसेल"""
    status = doc.get("status", "available")
    base = doc["name"]

    if status == "available":
        return f"{base} (Available)"
    elif status == "busy":
        delay = doc.get("delay_min", 10)
        return f"{base} (Busy, may be {delay} min late)"
    elif status == "unavailable":
        when = doc.get("available_on") or "later"
        return f"{base} (Unavailable until {when})"
    return base


def status_message(doc: dict):
    status = doc.get("status", "available")
    delay = doc.get("delay_min", 0)
    when = doc.get("available_on")

    if status == "available":
        return "🟢 Doctor is available."
    if status == "busy":
        return f"🟡 Doctor is currently busy, may be ~{delay} minutes late."
    if status == "unavailable":
        return f"🔴 Doctor is not available right now. Expected from: {when or 'later'}."
    return ""


def check_slot_for_doctor(doc: dict, time_str: str) -> bool:
    return time_str in doc.get("slots", [])


# --------------------- MAIN UI --------------------- #
def show_booking():
    from templates.auth import is_logged_in

    init_booking_table()
    st.subheader("📅 Patient Booking")

    if not is_logged_in():
        st.warning("🔐 Please login from the left sidebar to book an appointment.")
        return

    username = st.session_state.get("user", "guest")

    col1, col2 = st.columns(2)

    with col1:
        patient_name = st.text_input("Patient Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=25)
        specialization = st.selectbox(
            "Doctor Specialization",
            list(DOCTORS.keys()),
        )

    with col2:
        symptoms = st.text_area("Symptoms / Problem", height=120)
        date = st.date_input("Preferred Date")
        time_ = st.time_input("Preferred Time")

    st.markdown("---")
    st.subheader("👨‍⚕️ Choose Doctor")

    doctors_for_spec = DOCTORS.get(specialization, [])

    if not doctors_for_spec:
        st.error("No doctors configured for this specialization.")
        return

    # Doctor dropdown with status
    doctor_labels = [format_doctor_label(d) for d in doctors_for_spec]
    selected_index = st.selectbox(
        "Select Doctor",
        options=range(len(doctors_for_spec)),
        format_func=lambda i: doctor_labels[i],
    )
    selected_doc = doctors_for_spec[selected_index]

    # Show detailed status
    msg = status_message(selected_doc)
    if selected_doc["status"] == "available":
        st.success(msg)
    elif selected_doc["status"] == "busy":
        st.warning(msg)
    else:
        st.error(msg)

    # Show slots if any
    slots = selected_doc.get("slots", [])
    if slots:
        st.info(
            f"🕒 Available slots for **{selected_doc['name']}**: "
            + ", ".join(slots)
        )
    else:
        st.info(f"No predefined slots for {selected_doc['name']}.")

    # --------------------- BOOK BUTTON --------------------- #
    if st.button("✅ Confirm Booking"):
        if not patient_name.strip():
            st.warning("Please enter patient name.")
            return

        time_str = time_to_str(time_)

        # Doctor unavailable -> block booking
        if selected_doc["status"] == "unavailable":
            st.error(
                f"❌ {selected_doc['name']} is unavailable now. "
                f"Expected from: {selected_doc.get('available_on') or 'later'}."
            )
            return

        # Slot check
        if slots and not check_slot_for_doctor(selected_doc, time_str):
            st.error(
                f"❌ {selected_doc['name']} is not free at **{time_str}**."
            )
            st.info(
                "✅ Available slots: " + ", ".join(slots)
                if slots else "No predefined available slots."
            )
            return

        # Save booking
        save_appointment(
            username=username,
            patient_name=patient_name.strip(),
            age=int(age),
            specialization=specialization,
            doctor_name=selected_doc["name"],
            symptoms=symptoms.strip(),
            date=str(date),
            time_=time_str,
        )

        # Success message + delay info if busy
        if selected_doc["status"] == "busy":
            delay = selected_doc.get("delay_min", 10)
            st.success(
                f"🎉 Appointment booked with **{selected_doc['name']}** "
                f"on **{date} at {time_str}**.\n\n"
                f"🕒 Note: Doctor may be about **{delay} min** late."
            )
        else:
            st.success(
                f"🎉 Appointment booked with **{selected_doc['name']}** "
                f"on **{date} at {time_str}**."
            )

    # ---------------- RECENT APPOINTMENTS ---------------- #
    st.markdown("---")
    st.subheader("📋 Your Recent Appointments")

    rows = load_appointments(username=username)

    if not rows:
        st.info("No appointments yet.")
        return

    for appt in rows[:10]:
        (
            appt_id,
            pname,
            a,
            spec,
            doc_name,
            d,
            t,
            sym,
            created,
        ) = appt

        header = f"#{appt_id} - {pname} → {doc_name or 'Unknown'} ({spec}) on {d} at {t}"

        with st.expander(header):
            st.write(f"👤 **Patient:** {pname} (Age {a})")
            st.write(f"🩺 **Specialization:** {spec}")
            st.write(f"👨‍⚕️ **Doctor:** {doc_name or 'Not stored'}")
            st.write(f"📅 **Date:** {d}")
            st.write(f"⏰ **Time:** {t}")
            st.write(f"📝 **Symptoms:** {sym or '-'}")
            st.caption(f"Created at: {created}")
