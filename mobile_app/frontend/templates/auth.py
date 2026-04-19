import streamlit as st
import sqlite3
import os

# ---------------- DB PATH (SIMPLE + STABLE) ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "clinic.db")


# ---------------- INIT TABLE ----------------
def init_user_table():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        """)
        conn.commit()


# ---------------- CREATE USER ----------------
def create_user(username, password):
    username = username.strip().lower()
    password = password.strip()

    try:
        with sqlite3.connect(DB_PATH) as conn:
            conn.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


# ---------------- CHECK USER ----------------
def check_user(username, password):
    username = username.strip().lower()
    password = password.strip()

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute(
            "SELECT id FROM users WHERE username=? AND password=?",
            (username, password)
        )
        return cur.fetchone() is not None


# ---------------- LOGIN STATE ----------------
def is_logged_in():
    return st.session_state.get("user") is not None


# ---------------- SIDEBAR AUTH ----------------
def show_auth_sidebar():
    init_user_table()

    if "user" not in st.session_state:
        st.session_state["user"] = None

    st.sidebar.markdown("## 👤 Account")

    # -------- Already Logged In --------
    if is_logged_in():
        st.sidebar.success(f"Logged in as **{st.session_state['user']}**")

        if st.sidebar.button("Logout", key="logout_btn"):
            st.session_state["user"] = None
            st.rerun()
        return

    # -------- Mode --------
    mode = st.sidebar.radio("Mode", ["Login", "Signup"], key="auth_mode")

    # -------- LOGIN --------
    if mode == "Login":
        username = st.sidebar.text_input("Username", key="login_user")
        password = st.sidebar.text_input("Password", type="password", key="login_pass")

        if st.sidebar.button("Login", key="login_btn"):
            if not username or not password:
                st.sidebar.warning("⚠ Enter username & password")
            elif check_user(username, password):
                st.session_state["user"] = username.strip().lower()
                st.sidebar.success("✅ Login successful")
                st.rerun()
            else:
                st.sidebar.error("❌ Invalid username or password")

    # -------- SIGNUP --------
    else:
        username = st.sidebar.text_input("New Username", key="signup_user")
        password = st.sidebar.text_input("New Password", type="password", key="signup_pass")

        if st.sidebar.button("Create Account", key="signup_btn"):
            if not username or not password:
                st.sidebar.warning("⚠ Fill all fields")
            else:
                created = create_user(username, password)

                if created:
                    st.sidebar.success("✅ Account created! Now login.")
                else:
                    st.sidebar.error("❌ Username already exists")