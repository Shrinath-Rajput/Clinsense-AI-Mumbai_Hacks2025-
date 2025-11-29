

import streamlit as st
import os

# Import templates
from templates.home import show_home
from templates.booking import show_booking
from templates.dashboard import show_dashboard
from templates.smart_doctor_match import show_smart_match
from templates.chatbot import show_chatbot
from templates.image_tools import show_image_tools
from templates.voice_assistant import show_voice_assistant
from templates.auth import show_auth_sidebar, is_logged_in


# ----------------------- PAGE CONFIG -----------------------
st.set_page_config(
    page_title="ClinSense AI",
    layout="wide",
    page_icon="🩺"
)

# ----------------------- ADMIN LOGIN FLAG -----------------------
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False


def doctor_admin_login_box():
    st.sidebar.markdown("### 👨‍⚕ Doctor / Admin Login")

    admin_user = st.sidebar.text_input("Admin Username", key="adm_u")
    admin_pass = st.sidebar.text_input("Admin Password", key="adm_p", type="password")

    if st.sidebar.button("Admin Login"):
        if admin_user == "admin" and admin_pass == "clin@123":
            st.session_state["is_admin"] = True
            st.sidebar.success("Admin Login Successful!")
        else:
            st.sidebar.error("Invalid Admin Credentials")

    if st.sidebar.button("Logout Admin"):
        st.session_state["is_admin"] = False
        st.sidebar.info("Admin Logged Out")


# ----------------------- THEME STATE -----------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "Light"


def apply_theme():
    theme = st.session_state.get("theme", "Light")

    if theme == "Light":
        css = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #f4f7fc !important;
            color: #000 !important;
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
        }
        [data-testid="stSidebar"] * {
            color: #000 !important;
        }
        </style>
        """
    else:
        css = """
        <style>
        [data-testid="stAppViewContainer"] {
            background-color: #0a0a0a !important;
            color: #ffffff !important;
        }
        [data-testid="stSidebar"] {
            background-color: #111 !important;
        }
        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }
        </style>
        """

    st.markdown(css, unsafe_allow_html=True)


# Apply Theme
apply_theme()


# ----------------------- GLOBAL CSS FOR INPUT FIX -----------------------
st.markdown("""
<style>

input, textarea, select {
    background-color: #ffffff !important;
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border: 1px solid #777 !important;
    border-radius: 8px !important;
}

div[data-baseweb="select"] > div {
    background-color: #ffffff !important;
    color: #000 !important;
    -webkit-text-fill-color: #000 !important;
}

ul[role="listbox"] {
    background-color: #fff !important;
}

ul[role="listbox"] li {
    color: #000 !important;
}

ul[role="listbox"] li:hover {
    background-color: #e6f3ff !important;
}

input[type="time"] {
    color: #000 !important;
    -webkit-text-fill-color: #000 !important;
}

::placeholder {
    color: #555 !important;
}

</style>
""", unsafe_allow_html=True)


# ----------------------- LOAD styles.css -----------------------
css_path = os.path.join("assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ----------------------- HEADER -----------------------
col1, col2, col3 = st.columns([0.25, 0.50, 0.25])

with col2:
    st.image("assets/logo.png", width=230)
    st.markdown(
        "<h1 style='text-align:center;margin-bottom:0;'>ClinSense AI</h1>"
        "<p style='text-align:center;margin-top:2px;color:#777;'>Smart AI-powered Health & Appointment System.\n ClinSense Al is an advanced appointment-prioritization system that uses agentic Al to assess patient urgency, clinical factors, and real-time availability. It intelligently arranges appointments to reduce wait times, streamline hospital workflow, and ensure timely care for high-priority patients. The system offers a reliable, data-driven approach to improving overall healthcare efficiency.</p>",
        unsafe_allow_html=True,
    )

st.markdown("---")


# ----------------------- SIDEBAR -----------------------
show_auth_sidebar()
doctor_admin_login_box()

st.sidebar.markdown("---")

theme_choice = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])
if theme_choice != st.session_state["theme"]:
    st.session_state["theme"] = theme_choice
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Smart Doctor Match (AI)",
        "Patient Booking",
        "Doctor Dashboard",
        "AI Health Chatbot",
        "AI Image Tools",
        "AI Voice Assistant",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("⚠ Prototype only. Not a substitute for real doctors.")


# ----------------------- ROUTING -----------------------

# Protect Pages
patient_pages = ["Patient Booking"]
admin_pages = ["Doctor Dashboard"]

if page in patient_pages and not is_logged_in():
    st.warning("🔐 Please login as user to access this page.")

elif page in admin_pages and not st.session_state["is_admin"]:
    st.error("🚫 Admin Login Required.")

else:
    if page == "Home":
        show_home()

    elif page == "Smart Doctor Match (AI)":
        show_smart_match()

    elif page == "Patient Booking":
        show_booking()

    elif page == "Doctor Dashboard":
        show_dashboard()

    elif page == "AI Health Chatbot":
        show_chatbot()

    elif page == "AI Image Tools":
        show_image_tools()

    elif page == "AI Voice Assistant":
        show_voice_assistant()

    else:
        st.write("Page Not Found")