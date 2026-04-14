import streamlit as st
import os

# ---------------- SAFE IMPORTS ----------------
try:
    from mobile_app.frontend.templates.home import show_home
    from mobile_app.frontend.templates.booking import show_booking
    from mobile_app.frontend.templates.dashboard import show_dashboard
    from mobile_app.frontend.templates.smart_doctor_match import show_smart_match
    from mobile_app.frontend.templates.chatbot import show_chatbot
    from mobile_app.frontend.templates.image_tools import show_image_tools

    # voice assistant optional (openai issue avoid)
    try:
        from mobile_app.frontend.templates.voice_assistant import show_voice_assistant
    except:
        show_voice_assistant = None

    from mobile_app.frontend.templates.auth import show_auth_sidebar, is_logged_in

except Exception as e:
    st.error(f"❌ Import Error: {e}")
    st.stop()


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ClinSense AI",
    layout="wide",
    page_icon="🩺"
)

st.write("✅ App Started Successfully 🚀")


# ---------------- ADMIN LOGIN ----------------
if "is_admin" not in st.session_state:
    st.session_state["is_admin"] = False


def doctor_admin_login_box():
    st.sidebar.markdown("### 👨‍⚕ Doctor / Admin Login")

    admin_user = st.sidebar.text_input("Admin Username")
    admin_pass = st.sidebar.text_input("Admin Password", type="password")

    if st.sidebar.button("Admin Login"):
        if admin_user == "admin" and admin_pass == "clin@123":
            st.session_state["is_admin"] = True
            st.sidebar.success("Admin Login Successful!")
        else:
            st.sidebar.error("Invalid Admin Credentials")

    if st.sidebar.button("Logout Admin"):
        st.session_state["is_admin"] = False
        st.sidebar.info("Admin Logged Out")


# ---------------- CSS ----------------
css_path = os.path.join("mobile_app", "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


# ---------------- HEADER ----------------
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    logo_path = os.path.join("mobile_app", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=200)

    st.markdown("<h1 style='text-align:center;'>ClinSense AI</h1>", unsafe_allow_html=True)

st.markdown("---")


# ---------------- SIDEBAR ----------------
show_auth_sidebar()
doctor_admin_login_box()

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "Smart Doctor Match",
        "Patient Booking",
        "Doctor Dashboard",
        "Chatbot",
        "Image Tools",
        "Voice Assistant"
    ]
)


# ---------------- ROUTING ----------------
try:
    if page == "Home":
        show_home()

    elif page == "Smart Doctor Match":
        show_smart_match()

    elif page == "Patient Booking":
        if not is_logged_in():
            st.warning("🔐 Login required")
        else:
            show_booking()

    elif page == "Doctor Dashboard":
        if not st.session_state["is_admin"]:
            st.error("🚫 Admin Login Required")
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
            st.warning("⚠ Voice Assistant not available")

except Exception as e:
    st.error(f"❌ Runtime Error: {e}")