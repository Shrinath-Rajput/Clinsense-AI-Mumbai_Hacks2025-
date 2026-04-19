import streamlit as st
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "users.db")

# ---------------- INIT DB ----------------
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT
        )
        """)
        conn.commit()

# ---------------- CREATE USER ----------------
def create_user(username, password):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users VALUES (?, ?)",
                (username.strip(), password.strip())
            )
            conn.commit()
        return True
    except:
        return False

# ---------------- CHECK USER ----------------
def check_user(username, password):
    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username.strip(), password.strip())
        )
        return cur.fetchone() is not None

# ---------------- LOGIN STATE ----------------
def is_logged_in():
    return st.session_state.get("user") is not None

# ---------------- SIDEBAR ----------------
def show_auth_sidebar():
    init_db()

    if "user" not in st.session_state:
        st.session_state["user"] = None

    st.sidebar.subheader("👤 Account")

    # Already logged in
    if is_logged_in():
        st.sidebar.success(f"Logged in as {st.session_state['user']}")

        if st.sidebar.button("Logout"):
            st.session_state["user"] = None
            st.rerun()
        return

    mode = st.sidebar.radio("Mode", ["Login", "Signup"])

    if mode == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")

        if st.sidebar.button("Login"):
            if check_user(username, password):
                st.session_state["user"] = username
                st.sidebar.success("Login successful 🎉")
                st.rerun()
            else:
                st.sidebar.error("Invalid username or password ❌")

    else:
        username = st.sidebar.text_input("New Username")
        password = st.sidebar.text_input("New Password", type="password")

        if st.sidebar.button("Create Account"):
            if create_user(username, password):
                st.sidebar.success("Account created ✅")
            else:
                st.sidebar.error("User already exists ❌")