# frontend/templates/voice_assistant.py

import os
import streamlit as st
from openai import OpenAI

@st.cache_resource
def get_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set in environment variables.")
    return OpenAI(api_key=api_key)

def show_voice_assistant():
    st.subheader("🎙 AI Voice Assistant (Prototype)")

    st.info(
        "Speak commands like:\n"
        "- 'Book appointment with cardiologist tomorrow at 5 PM'\n"
        "- 'I have chest pain and breathing issue'\n\n"
        "Prototype: converts voice → text using Whisper, then processes it as a health query."
    )

    audio_file = st.file_uploader(
        "Upload voice recording (wav, mp3, m4a)",
        type=["wav", "mp3", "m4a"],
    )

    if audio_file is not None:
        st.audio(audio_file)

        if st.button("🧠 Transcribe & Understand"):
            try:
                client = get_client()
                with st.spinner("Transcribing with Whisper..."):
                    transcript = client.audio.transcriptions.create(
                        model="gpt-4o-mini-tts",  # adjust to current audio model name if needed
                        file=audio_file,
                    )

                text = transcript.text
                st.success("Transcription:")
                st.write(text)

                st.markdown("---")
                st.write("Now sending this to the AI health assistant...")

                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions=(
                        "You are an assistant that converts patient voice requests "
                        "into clear actions like 'book appointment with cardiologist', "
                        "'show nearby hospitals', etc. Do NOT actually book anything, "
                        "just describe the action in 2-3 lines."
                    ),
                    input=text,
                )

                st.subheader("🧾 Detected Intent (Demo)")
                st.write(response.output_text)

            except Exception as e:
                st.error(f"Error in voice processing: {e}")
