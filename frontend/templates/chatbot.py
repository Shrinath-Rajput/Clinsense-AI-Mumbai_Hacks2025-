import streamlit as st

def show_chatbot():
    st.title("🧠 AI Health Chatbot")

    st.write("Ask health-related questions. This is a demo chatbot page.")

    user_input = st.text_area("Your Question:", height=120)

    if st.button("Ask AI"):
        if not user_input.strip():
            st.warning("Please enter a question.")
            return

        # For now, dummy AI reply
        reply = "This is a demo AI reply. Full model will be connected later."

        st.success(reply)
