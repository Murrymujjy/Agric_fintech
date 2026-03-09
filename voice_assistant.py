import streamlit as st
import joblib
import numpy as np
from openai import OpenAI
import speech_recognition as sr
import io

def render():
    # Mapping for Google Speech API
    lang_codes = {
        "English": "en-US", "Luganda (Uganda)": "lg-UG", "Yoruba (Nigeria)": "yo-NG",
        "Hausa (Nigeria)": "ha-NG", "Swahili (East Africa)": "sw-KE"
    }
    
    current_lang = st.session_state.lang
    code = lang_codes.get(current_lang, "en-US")

    st.title(f"🎙️ Voice Assistant ({current_lang})")
    st.write(f"Please speak clearly in {current_lang}.")

    audio_file = st.audio_input("Record your profile")

    if audio_file:
        with st.spinner("Processing..."):
            r = sr.Recognizer()
            try:
                audio_bytes = audio_file.read()
                with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                    audio_content = r.record(source)
                
                # Transcribe using selected African Language Code
                user_text = r.recognize_google(audio_content, language=code)
                st.success(f"**Transcribed:** {user_text}")
                
                # (Include your Featherless.ai / ML logic here as before)
                
            except Exception:
                st.error("❌ Voice not recognized.")
                st.info("💡 Pro Tip: Our chatbot is more stable for text entry. Try it instead!")
                if st.button("Switch to Chatbot"):
                    st.session_state.selected_nav = "🤖 Chatbot"
                    st.rerun()
