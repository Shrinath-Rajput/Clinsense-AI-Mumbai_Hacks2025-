# frontend/templates/auth.py

import streamlit as st
import sqlite3
import os
from datetime import datetime

# ----------------------- DATABASE PATH -----------------------
DB_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
DB_PATH = os.path.join(DB_DIR, "clinic.db")


# ----------------------- INIT TABLE -----------------------
def init_user_table():
    os.makedirs(DB_DIR, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT,
                created_at TEXT
            )
            """
        )
        conn.commit()


# ----------------------- CREATE USER -----------------------
def create_user(username: str, password: str) -> bool:
    init_user_table()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (username, password, created_at) VALUES (?, ?, ?)",
                (username, password, datetime.now().isoformat()),
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# ----------------------- CHECK USER -----------------------
def check_user(username: str, password: str) -> bool:
    init_user_table()

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, password),
        )
        row = cur.fetchone()

    return row is not None


# ----------------------- LOGIN STATE -----------------------
def is_logged_in() -> bool:
    return st.session_state.get("user") is not None


# ----------------------- SIDEBAR AUTH -----------------------
def show_auth_sidebar():
    init_user_table()

    if "user" not in st.session_state:
        st.session_state["user"] = None

    st.sidebar.subheader("👤 Account")

    # Already logged in
    if is_logged_in():
        st.sidebar.success(f"Logged in as **{st.session_state['user']}**")

        if st.sidebar.button("Logout"):
            st.session_state["user"] = None
            st.rerun()   # UPDATED FOR NEW STREAMLIT
        return

    # Not logged in
    mode = st.sidebar.radio("Mode", ["Login", "Signup"])

    if mode == "Login":
        username = st.sidebar.text_input("Username", key="login_user")
        password = st.sidebar.text_input("Password", type="password", key="login_pass")

        if st.sidebar.button("Login"):
            if check_user(username, password):
                st.session_state["user"] = username
                st.sidebar.success("Login successful! 🎉")
                st.rerun()    # UPDATED
            else:
                st.sidebar.error("Invalid username or password ❌")

    else:  # Signup mode
        username = st.sidebar.text_input("New Username", key="signup_user")
        password = st.sidebar.text_input("New Password", type="password", key="signup_pass")

        if st.sidebar.button("Create Account"):
            if not username or not password:
                st.sidebar.warning("Please fill all fields.")
            else:
                created = create_user(username, password)
                if created:
                    st.sidebar.success("Account created! Now login 👍")
                else:
                    st.sidebar.error("Username already exists ❌")
