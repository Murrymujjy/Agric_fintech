import streamlit as st
import joblib
import numpy as np
from openai import OpenAI

def render():
    st.title("🎙️ Voice-Activated Credit Profiler")
    st.markdown("""
    **Accessibility Feature:** Designed to bridge the literacy gap for rural farmers. 
    By speaking naturally, our hybrid AI extracts financial data and provides instant scoring.
    """)

    # --- API Orchestration ---
    # Client 1: Standard OpenAI for Transcription (Whisper) - avoids the 404 error
    if "OPENAI_API_KEY" in st.secrets:
        audio_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("Missing OPENAI_API_KEY in secrets.toml")
        return

    # Client 2: Featherless.ai for High-Performance LLM Reasoning (Llama 3.1)
    llm_client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    # Load the local Decision Engine
    try:
        model = joblib.load("models_logistic_regression_model.pkl")
    except Exception as e:
        st.error(f"Model file error: {e}. Check if the .pkl file exists in your directory.")
        return

    # --- Step 1: Voice Input ---
    audio_file = st.audio_input("Describe your profile (Age, Sector, Education, Phone Access)")

    if audio_file:
        # Essential file pointer reset and naming for API compatibility
        audio_file.name = "recording.wav" 
        audio_file.seek(0) 

        with st.spinner("Step 1: Transcribing voice via Whisper..."):
            try:
                # Transcribe using specialized audio endpoint
                transcript = audio_client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
                user_text = transcript.text
                st.info(f"**Transcribed Text:** {user_text}")

                with st.spinner("Step 2: Extracting data via Llama 3.1 (Featherless)..."):
                    # Use LLM to bridge unstructured speech to structured data
                    extract_prompt = f"""
                    Extract 6 numerical features from this farmer's statement: "{user_text}". 
                    Features: [Age, YearsInCommunity, Education(0-8), HasPhone(0/1), Rural(1)/Urban(0), WomenSupport(0/1)]
                    Return ONLY a Python list. Example: [30, 5, 4, 1, 1, 0]
                    """
                    
                    extraction = llm_client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[{"role": "user", "content": extract_prompt}],
                        max_tokens=200 # Kept low for speed and stability
                    )
                    
                    # Clean and parse the AI response
                    raw_list = extraction.choices[0].message.content.strip()
                    clean_list = raw_list.replace("```python", "").replace("```", "").strip()
                    data_list = eval(clean_list)
                    X = np.array([data_list])

                # --- Step 3: Predictive Analysis ---
                prediction = model.predict(X)[0]
                prob = model.predict_proba(X)[0][1]

                st.subheader("📊 Instant Credit Assessment")
                if prediction == 1:
                    st.success(f"✅ Approved | Approval Confidence: {prob:.2f}")
                else:
                    st.error(f"⚠️ High Risk | Approval Confidence: {prob:.2f}")

                # Step 4: Generative Explainability (The 'Why')
                explain_prompt = f"Explain why a farmer with these stats was {'approved' if prediction == 1 else 'denied'}: {user_text}. Give one tip."
                explanation = llm_client.chat.completions.create(
                    model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                    messages=[{"role": "user", "content": explain_prompt}],
                    max_tokens=500
                )
                st.write(f"**AI Insight:** {explanation.choices[0].message.content}")

            except Exception as e:
                st.error(f"Pipeline Error: {e}")
                st.info("Technical Tip: Ensure your OpenAI key has credits for the Whisper model.")

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Integrated Hybrid AI Pipeline | <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)
