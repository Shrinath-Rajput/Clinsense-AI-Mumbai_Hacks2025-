import sys
import os

# mobile_app path add
sys.path.append(os.path.join(os.path.dirname(__file__), "mobile_app"))

import streamlit as st

# SAFE IMPORTS
try:
    from frontend.templates.home import show_home
    from frontend.templates.booking import show_booking
    from frontend.templates.dashboard import show_dashboard
    from frontend.templates.smart_doctor_match import show_smart_match
    from frontend.templates.chatbot import show_chatbot
    from frontend.templates.image_tools import show_image_tools

    try:
        from frontend.templates.voice_assistant import show_voice_assistant
    except:
        show_voice_assistant = None

    from frontend.templates.auth import show_auth_sidebar, is_logged_in

except Exception as e:
    st.error(f"❌ Import Error: {e}")
    st.stop()


# PAGE CONFIG
st.set_page_config(page_title="ClinSense AI", layout="wide")
st.title("🩺 ClinSense AI")


# ADMIN STATE
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False


def admin_login():
    st.sidebar.markdown("### 👨‍⚕ Admin Login")

    user = st.sidebar.text_input("Username")
    pwd = st.sidebar.text_input("Password", type="password")

    if st.sidebar.button("Login", key="admin_login_btn"):
        if user == "admin" and pwd == "clin@123":
            st.session_state["is_admin"] = True
            st.success("✅ Logged in")
        else:
            st.error("❌ Invalid")

    if st.sidebar.button("Logout", key="admin_logout_btn"):
        st.session_state["is_admin"] = False
        st.info("Logged out")


# SIDEBAR
show_auth_sidebar()
admin_login()

page = st.sidebar.radio(
    "Navigation",
    [
        "Home",
        "Smart Doctor Match",
        "Booking",
        "Dashboard",
        "Chatbot",
        "Image Tools",
        "Voice Assistant"
    ]
)


# ROUTING
try:
    if page == "Home":
        show_home()

    elif page == "Smart Doctor Match":
        show_smart_match()

    elif page == "Booking":
        if not is_logged_in():
            st.warning("Login required")
        else:
            show_booking()

    elif page == "Dashboard":
        if not st.session_state["is_admin"]:
            st.error("Admin login required")
        else:
            show_dashboard()

    elif page == "Chatbot":
        show_chatbot()

    elif page == "Image Tools":
        show_image_tools()

    elif page == "Voice Assistant":
        if show_voice_assistant:
            show_voice_assistant()
        else:
            st.warning("Not available")

except Exception as e:
    st.error(f"❌ Runtime Error: {e}")