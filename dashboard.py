# frontend/templates/dashboard.py

import streamlit as st
import sqlite3
import os
from datetime import datetime, timedelta

from templates.booking import DOCTORS   # <-- ALL DOCTORS IMPORTED

DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "clinic.db")


def load_all_appointments():
    if not os.path.exists(DB_PATH):
        return []

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            """
            SELECT id, patient_name, age, specialization, doctor_name,
                   date, time, symptoms, created_at
            FROM appointments
            ORDER BY date, time
            """
        )
        return cur.fetchall()


def get_all_doctor_names(rows):
    db_doctors = {r[4] for r in rows if r[4]}

    # doctors from DOCTORS dictionary
    dict_doctors = set()
    for spec, docs in DOCTORS.items():
        for d in docs:
            dict_doctors.add(d["name"])

    # merge both
    return sorted(list(db_doctors | dict_doctors))


def detect_delay(appointments):
    delay_notice = []
    doc_map = {}

    for appt in appointments:
        doc = appt[4]
        d = appt[5]
        t = appt[6]
        if not doc:
            continue
        doc_map.setdefault(doc, []).append(f"{d} {t}")

    for doc, times in doc_map.items():
        counts = {}
        for slot in times:
            counts[slot] = counts.get(slot, 0) + 1

        total_delay = sum(v - 1 for v in counts.values() if v > 1)
        if total_delay > 0:
            delay_notice.append((doc, total_delay * 10))

    return delay_notice


def show_dashboard():
    st.subheader("🩺 Doctor Dashboard")

    rows = load_all_appointments()

    doctor_names = get_all_doctor_names(rows)

    selected_doc = st.selectbox(
        "Filter by Doctor",
        ["All doctors"] + doctor_names,
    )

    # Delay detection
    delays = detect_delay(rows)
    for doc, mins in delays:
        st.warning(f"⚠ {doc} may be {mins} minutes late due to back-to-back appointments.")

    st.markdown("---")

    # show all appointments
    for appt in rows:
        (
            appt_id, pname, age, spec, doc_name,
            d, t, sym, created
        ) = appt

        if selected_doc != "All doctors" and doc_name != selected_doc:
            continue

        title = f"#{appt_id} | {pname} → {doc_name or 'Unassigned'} on {d} at {t}"

        with st.expander(title):
            st.write(f"👤 **Patient:** {pname} (Age {age})")
            st.write(f"🩺 **Specialization:** {spec}")
            st.write(f"👨‍⚕️ **Doctor:** {doc_name or 'Not assigned'}")
            st.write(f"📅 **Date:** {d}")
            st.write(f"⏰ **Time:** {t}")
            st.write(f"📝 **Symptoms:** {sym or '-'}")
            st.caption(f"Created at: {created}")

    st.success("Dashboard loaded successfully ✔")
