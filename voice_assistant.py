import streamlit as st
import joblib
import numpy as np
from openai import OpenAI
import speech_recognition as sr
import io

def render():
    st.title("🎙️ Voice-Activated Credit Profiler")
    st.markdown("""
    **Accessibility Feature:** Designed for rural financial inclusion. 
    This module uses a free speech-to-text fallback to ensure 100% uptime for farmers.
    """)

    # Client for Featherless.ai (Using your active $11 credit balance)
    llm_client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    # Load the Predictive Engine
    try:
        model = joblib.load("models_logistic_regression_model.pkl")
    except Exception as e:
        st.error(f"Predictive Model not found: {e}")
        return

    # Step 1: Voice Input
    audio_file = st.audio_input("Describe your profile (Age, Education, Location)")

    if audio_file:
        with st.spinner("Step 1: Transcribing voice (Free Fallback)..."):
            try:
                # Initialize Recognizer
                r = sr.Recognizer()
                
                # Convert Streamlit Audio to a format SpeechRecognition understands
                audio_data = sr.AudioFile(audio_file)
                with audio_data as source:
                    audio_content = r.record(source)
                
                # Use Google's Free Web Speech API (No Key Required)
                user_text = r.recognize_google(audio_content)
                st.info(f"**Transcribed:** {user_text}")

                with st.spinner("Step 2: Extracting data via Llama 3.1 (Featherless)..."):
                    # Use Featherless for the 'Thinking' part
                    extract_prompt = f"""
                    Extract 6 numerical features from: "{user_text}". 
                    Format: [Age, YearsInCommunity, Education(0-8), Phone(0/1), Rural(1)/Urban(0), WomenSupport(0/1)]
                    Return ONLY the list. Example: [35, 10, 4, 1, 1, 0]
                    """
                    
                    extraction = llm_client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[{"role": "user", "content": extract_prompt}],
                        max_tokens=200
                    )
                    
                    # Parse extraction
                    raw_list = extraction.choices[0].message.content.strip()
                    clean_list = raw_list.replace("```python", "").replace("```", "").strip()
                    data_list = eval(clean_list)
                    X = np.array([data_list])

                # Step 3: Predictive Analysis [cite: 2026-03-02]
                prediction = model.predict(X)[0]
                prob = model.predict_proba(X)[0][1]

                st.subheader("📊 Credit Assessment Result")
                if prediction == 1:
                    st.success(f"✅ Approved | Confidence: {prob:.2f}")
                else:
                    st.error(f"⚠️ High Risk | Confidence: {prob:.2f}")

                # Step 4: Explanation via Featherless
                explain_prompt = f"Explain this result based on the transcript: '{user_text}'. Result: {'Approved' if prediction == 1 else 'Denied'}."
                explanation = llm_client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": explain_prompt}],
                    max_tokens=500
                )
                st.write(f"**AI Insight:** {explanation.choices[0].message.content}")

            except Exception as e:
                st.error(f"Voice Processing Error: {e}")
                st.info("Ensure your internet connection is stable for the free transcription service.")

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Hybrid AI Architecture | <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)
