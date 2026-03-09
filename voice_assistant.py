import streamlit as st
import joblib
import numpy as np
from openai import OpenAI
import speech_recognition as sr
import io

def render():
    st.title("🎙️ Voice-Activated Credit Profiler")
    
    # Featherless Client (Using your $11 credit balance)
    llm_client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    try:
        model = joblib.load("models_logistic_regression_model.pkl")
    except Exception as e:
        st.error(f"Predictive Model not found: {e}")
        return

    audio_file = st.audio_input("Record your details clearly (Age, Education, Sector)")

    if audio_file:
        with st.spinner("Processing Voice..."):
            try:
                # Initialize Recognizer
                r = sr.Recognizer()
                
                # Convert the Streamlit UploadedFile to a BytesIO object for SpeechRecognition
                audio_bytes = audio_file.read()
                audio_data_io = io.BytesIO(audio_bytes)
                
                with sr.AudioFile(audio_data_io) as source:
                    # Adjust for ambient noise to improve accuracy
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    audio_content = r.record(source)
                
                # Attempt Transcription
                user_text = r.recognize_google(audio_content)
                st.info(f"**Transcribed:** {user_text}")

                # --- LLM Data Extraction ---
                extract_prompt = f"""
                Extract 6 features from: "{user_text}". 
                Format as a list: [Age, YearsInCommunity, Education(0-8), Phone(0/1), Rural(1)/Urban(0), WomenSupport(0/1)]
                Return ONLY the list. Example: [35, 10, 4, 1, 1, 0]
                """
                
                extraction = llm_client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": extract_prompt}],
                    max_tokens=200
                )
                
                data_list = eval(extraction.choices[0].message.content.strip().strip('`'))
                X = np.array([data_list])

                # --- Prediction ---
                prediction = model.predict(X)[0]
                prob = model.predict_proba(X)[0][1]

                st.subheader("📊 Credit Assessment Result")
                if prediction == 1:
                    st.success(f"✅ Approved | Confidence: {prob:.2f}")
                else:
                    st.error(f"⚠️ High Risk | Confidence: {prob:.2f}")

                # Explanation via Featherless
                explain_prompt = f"Explain this result based on the transcript: '{user_text}'. Result: {'Approved' if prediction == 1 else 'Denied'}."
                explanation = llm_client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": explain_prompt}],
                    max_tokens=500
                )
                st.write(f"**AI Insight:** {explanation.choices[0].message.content}")

            except sr.UnknownValueError:
                st.error("Could not understand the audio. Please speak more clearly.")
            except sr.RequestError as e:
                st.error(f"Could not request results from Google Speech Recognition service; {e}")
            except Exception as e:
                st.error(f"Voice Processing Error: {e}")
