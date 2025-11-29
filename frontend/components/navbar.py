import streamlit as st

def navbar():
    st.markdown("""
    <div class="navbar">
        <div class="brand">
            <img src="frontend/assets/logo.png" width="40px" style="vertical-align: middle; margin-right:10px;">
            <span style="font-size:22px; font-weight:bold;">ClinSense AI</span>
        </div>
        <div class="menu">
            <a href="#">Home</a>
            <a href="#">Book</a>
            <a href="#">Dashboard</a>
            <a href="#">Contact</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
