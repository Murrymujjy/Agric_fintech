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
    
    # Load ML Model (Ensure the filename matches your file system)
    try:
        model = joblib.load("models_logistic_regression_model.pkl")
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return

    # --- Step 1: Voice Input ---
    # st.audio_input provides the recording interface
    audio_file = st.audio_input("Record your profile (e.g., 'I am 45 years old, I live in a rural area and have a secondary education')")

    if audio_file:
        # --- THE CRITICAL FIXES ---
        # 1. Provide a name with extension so the API identifies the format
        audio_file.name = "recording.wav" 
        # 2. Reset the pointer to the start of the file for reading
        audio_file.seek(0) 

        with st.spinner("Processing your voice..."):
            try:
                # A. Transcribe Voice to Text using Whisper
                transcript = client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                user_text = transcript.text
                st.info(f"**Transcribed:** {user_text}")

                # B. Use LLM to extract data points for the ML Model
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
                    messages=[{"role": "user", "content": extract_prompt}],
                    max_tokens=500 # Kept low to avoid context window errors
                )
                
                # Convert string response to Python list
                raw_list = extraction.choices[0].message.content.strip()
                # Clean potential backticks if the AI wraps it in markdown
                clean_list = raw_list.replace("```python", "").replace("```", "").strip()
                data_list = eval(clean_list)
                X = np.array([data_list])

                # C. Run Prediction using Logistic Regression
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
                st.error(f"Processing Error: {e}")
                st.write("Check your API key in secrets.toml or ensure your internet connection is stable.")

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)
