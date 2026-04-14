import streamlit as st

def feature_cards():
    st.markdown("""
    <div class="card-container">
        <div class="card">
            <h3>AI Diagnosis</h3>
            <p>Get instant AI-based symptom analysis and possible causes.</p>
        </div>
        <div class="card">
            <h3>Doctor Booking</h3>
            <p>Book nearby doctors and get real-time waiting time updates.</p>
        </div>
        <div class="card">
            <h3>Notifications</h3>
            <p>Receive live updates on appointments and lab results.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
