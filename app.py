import sys
import os

# mobile_app folder path add करतोय
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


# SIDEBAR
show_auth_sidebar()

page = st.sidebar.radio(
    "Go to",
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
        show_dashboard()

    elif page == "Chatbot":
        show_chatbot()

    elif page == "Image Tools":
        show_image_tools()

    elif page == "Voice Assistant":
        if show_voice_assistant:
            show_voice_assistant()
        else:
            st.warning("Voice Assistant not available")

except Exception as e:
    st.error(f"❌ Runtime Error: {e}")