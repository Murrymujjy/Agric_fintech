import streamlit as st
import joblib
import numpy as np
from openai import OpenAI
import speech_recognition as sr
import io

def render():
    # 1. API & Model Setup
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    try:
        model = joblib.load("models_logistic_regression_model.pkl") # [cite: 2026-03-02]
    except Exception as e:
        st.error(f"Error loading prediction model: {e}")
        return

    # 2. Global Language Sync [cite: 2025-12-20]
    current_lang = st.session_state.lang
    
    # Mapping languages to Google Speech codes
    lang_codes = {
        "English": "en-US",
        "Luganda (Uganda)": "lg-UG",
        "Yoruba (Nigeria)": "yo-NG",
        "Hausa (Nigeria)": "ha-NG",
        "Igbo (Nigeria)": "ig-NG",
        "Swahili (East Africa)": "sw-KE",
        "Zulu (South Africa)": "zu-ZA",
        "Amharic (Ethiopia)": "am-ET",
        "Wolof (Senegal)": "wo-SN",
        "Afrikaans (South Africa)": "af-ZA"
    }
    
    lang_code = lang_codes.get(current_lang, "en-US")

    st.title(f"🎙️ {current_lang} Voice Assistant")
    st.markdown(f"**Instructions:** Please speak clearly in **{current_lang}**. Mention your age, how long you've lived in your community, education level, and if you have phone access.")

    # 3. Audio Input Widget
    audio_file = st.audio_input("Click to start recording")

    if audio_file:
        with st.spinner(f"Analyzing your {current_lang} speech..."):
            r = sr.Recognizer()
            try:
                # Process Audio for Transcription
                audio_bytes = audio_file.read()
                audio_io = io.BytesIO(audio_bytes)
                
                with sr.AudioFile(audio_io) as source:
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio_content = r.record(source)
                
                # Transcribe using the specific African Language Code [cite: 2026-03-02]
                user_text = r.recognize_google(audio_content, language=lang_code)
                st.success(f"**Transcribed Text:** {user_text}")

                # 4. LLM Data Extraction (Featherless.ai)
                # We ask the LLM to understand the text regardless of the language used
                extract_prompt = f"""
                Extract the following 6 features from this transcript: "{user_text}". 
                Transcript Language: {current_lang}
                Features: [Age, YearsInCommunity, Education(0-8), HasPhone(0/1), Rural(1)/Urban(0), WomenSupport(0/1)]
                Return ONLY the list. Example: [35, 10, 4, 1, 1, 0]
                """
                
                extraction = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": extract_prompt}],
                    max_tokens=200
                )
                
                # Parse output to list
                raw_list = extraction.choices[0].message.content.strip().strip('`')
                data_list = eval(raw_list.replace("```python", "").replace("```", ""))
                X = np.array([data_list])

                # 5. ML Prediction [cite: 2026-03-02]
                prediction = model.predict(X)[0]
                prob = model.predict_proba(X)[0][1]

                st.subheader("🏁 Assessment Result")
                if prediction == 1:
                    st.success(f"✅ Approved | Score: {prob:.2f}")
                else:
                    st.error(f"⚠️ High Risk | Score: {prob:.2f}")

                # 6. Localized Explanation
                explain_prompt = f"Explain this credit result in {current_lang} to the farmer. Result: {'Approved' if prediction == 1 else 'Denied'}. Original speech: {user_text}"
                explanation = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": explain_prompt}],
                    max_tokens=500
                )
                st.write(f"**AI Insight ({current_lang}):** {explanation.choices[0].message.content}")

            except Exception as e:
                st.error("❌ Could not process voice.")
                st.info("💡 **Fallback:** Please use the Chatbot for manual text entry.")
                if st.button("Switch to Chatbot"):
                    st.session_state.selected_nav = "🤖 Chatbot"
                    st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Pan-African Credit Engine | <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)
