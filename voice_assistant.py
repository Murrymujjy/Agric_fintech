import streamlit as st
import joblib
import numpy as np
from openai import OpenAI

def render():
    st.title("🎙️ Voice-Activated Credit Profiler")
    st.markdown("""
    **Accessibility Feature:** Specifically designed for rural farmers who prefer speaking over typing. 
    Our AI extracts key financial parameters directly from your voice.
    """)

    # Initialize Featherless Client
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    # Load ML Model
    model = joblib.load("models_logistic_regression_model.pkl")

    # --- Step 1: Voice Input ---
    audio_file = st.audio_input("Record your profile (e.g., 'I am 45 years old, I live in a rural area and have a secondary education')")

    if audio_file:
        with st.spinner("Processing your voice..."):
            try:
                # A. Transcribe Voice to Text
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                user_text = transcript.text
                st.info(f"**Transcribed:** {user_text}")

                # B. Use LLM to extract data points
                # We force the LLM to return a clean list for our ML model
                extract_prompt = f"""
                Analyze the following text and extract these 6 features for a credit model:
                1. Age (int)
                2. Years in community (default to 5 if unknown)
                3. Education (0=None, 4=Secondary, 6=Degree)
                4. Has Phone (1 for yes, 0 for no)
                5. Sector (1 for rural, 0 for urban)
                6. Women Support (1 for yes, 0 for no)

                Text: "{user_text}"
                Return ONLY a Python list of integers. Example: [35, 10, 4, 1, 1, 0]
                """
                
                extraction = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": extract_prompt}]
                )
                
                # Convert string response to Python list
                raw_list = extraction.choices[0].message.content
                data_list = eval(raw_list)
                X = np.array([data_list])

                # C. Run Prediction
                prediction = model.predict(X)[0]
                prob = model.predict_proba(X)[0][1]

                # D. Generate AI Explanation
                st.subheader("Results")
                if prediction == 1:
                    st.success(f"✅ Approved (Confidence: {prob:.2f})")
                else:
                    st.error(f"⚠️ High Risk (Confidence: {prob:.2f})")

                explain_prompt = f"The farmer was { 'approved' if prediction == 1 else 'flagged as high risk' } based on this voice input: '{user_text}'. Briefly explain why in one sentence."
                explanation = client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": explain_prompt}],
                    max_tokens=500
                )
                st.write(explanation.choices[0].message.content)

            except Exception as e:
                st.error("There was an issue processing the audio. Please ensure your microphone is clear and the API key is valid.")
