import streamlit as st

def show_home():

    st.markdown(
        """
        <style>

            /* GLOBAL */
            body {
                margin:0;
                padding:0;
            }

            /* === HERO SECTION (Gradient Background) === */
            .hero-section {
                text-align: center;
                padding: 80px 20px;
                background: linear-gradient(135deg, #1a73e8, #00c6ff);
                color: white;
                border-radius: 18px;
                margin-bottom: 40px;
            }

            .hero-title {
                font-size: 52px;
                font-weight: 900;
                margin-bottom: 10px;
            }

            .hero-subtitle {
                font-size: 22px;
                opacity: 0.9;
                margin-bottom: 32px;
            }

            /* BUTTONS */
            .btn-primary {
                padding: 14px 34px;
                background: #ffffff;
                color: #1a73e8 !important;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 600;
                text-decoration: none;
                margin-right: 15px;
                transition: 0.3s;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .btn-primary:hover {
                background: #e3f0ff;
                transform: scale(1.05);
            }

            .btn-secondary {
                padding: 14px 34px;
                background: #ffc400;
                color: black !important;
                border-radius: 10px;
                font-size: 18px;
                font-weight: 600;
                text-decoration: none;
                transition: 0.3s;
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .btn-secondary:hover {
                background: #ffdd66;
                transform: scale(1.05);
            }

            /* === FEATURE CARDS (Glassmorphism) === */
            .feature-box {
                background: rgba(255,255,255,0.40);
                backdrop-filter: blur(12px);
                padding: 22px;
                border-radius: 18px;
                box-shadow: 0 6px 20px rgba(0,0,0,0.08);
                transition: 0.3s;
            }
            .feature-box:hover {
                transform: translateY(-6px);
                box-shadow: 0 10px 28px rgba(0,0,0,0.15);
            }

            .feature-title {
                font-size: 22px;
                font-weight: 700;
                margin-bottom: 6px;
            }
            .feature-text {
                font-size: 15px;
                color: #444;
            }

            /* FOOTER */
            .footer {
                margin-top: 60px;
                text-align: center;
                padding: 15px 0;
                color: #555;
                border-top: 1px solid #ddd;
                font-size: 14px;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

    # ---------- HERO SECTION ----------
    st.markdown(
        """
        <div class="hero-section">
            <h1 class="hero-title">ClinSense AI</h1>
            <p class="hero-subtitle">Smart AI-powered Health & Appointment System</p>

            
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------- FEATURES ----------
    st.markdown('<h2 id="features">✨ Key Features</h2>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-box">
                <h3 class="feature-title">🧠 AI Diagnosis</h3>
                <p class="feature-text">Analyzes symptoms & predicts best doctor.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-box">
                <h3 class="feature-title">📅 Smart Scheduling</h3>
                <p class="feature-text">Avoid rush & get perfect timeslot automatically.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-box">
                <h3 class="feature-title">🔔 Live Notifications</h3>
                <p class="feature-text">Get delay alerts & appointment reminders.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("---")

    # ---------- ABOUT SECTION ----------
    st.markdown("### 🩺 Why ClinSense AI?")
    st.write(
        """
        - Predicts best doctor specialization  
        - Reduces hospital waiting time  
        - Real-time doctor status & live alerts  
        - AI-driven symptom analysis  
        - Smart & modern healthcare experience  
        """
    )

    # ---------- FOOTER ----------
    st.markdown(
        """
        <div class="footer">
            © 2025 ClinSense AI — Developed by <b>Shrinath Rajput</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
