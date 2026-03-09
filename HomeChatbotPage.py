import streamlit as st
import joblib
import numpy as np
import re
from openai import OpenAI

def render():
    # 1. Initialize Featherless Client
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )

    # 2. Load the Local ML Model
    # Since you mentioned using a logistic regression model, we load that here.
    model = joblib.load("models_logistic_regression_model.pkl")

    st.title("🤖 AI Chatbot for Farmer Credit Scoring")
    st.markdown("I use **Logistic Regression** for accuracy and **Featherless.ai** for explanations.")

    # Session State for Chat History
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! Describe a farmer's profile (age, education, location), and I'll predict their loan eligibility."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 3. Enhanced Input Parsing
    def parse_user_intent(text):
        text = text.lower()
        # Regex to find age
        age_match = re.search(r"(\d+)\s*year", text)
        age = int(age_match.group(1)) if age_match else 30
        
        # Simple keyword extraction for the ML features
        education_map = {'primary': 2, 'secondary': 4, 'tertiary': 6, 'degree': 6}
        edu_val = 8 # Default 'Other'
        for key, val in education_map.items():
            if key in text:
                edu_val = val
                break
        
        sector = 1 if "rural" in text else 0
        phone = 1 if "phone" in text else 0
        women_support = 1 if "woman" in text or "support" in text else 0
        years_community = 5 # Default
        
        return np.array([[age, years_community, edu_val, phone, sector, women_support]]), {
            "age": age, "education": "Specified" if edu_val != 8 else "General", "sector": "Rural" if sector == 1 else "Urban"
        }

    # 4. Chat Logic
    prompt = st.chat_input("Ex: Will a 35 year old farmer in a rural area with secondary education get a loan?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing profile and generating insights..."):
                try:
                    # Step A: Get data for ML Model
                    X, meta = parse_user_intent(prompt)
                    
                    # Step B: Get ML Prediction
                    prediction = model.predict(X)[0]
                    prob = model.predict_proba(X)[0][1]
                    status = "Approved" if prediction == 1 else "High Risk"

                    # Step C: Use Featherless.ai to explain the 'Why'
                    # We pass the ML result to the LLM to make it "Functional"
                    ai_prompt = f"""
                    The Credit Model result for this farmer is: {status} (Confidence: {prob:.2f}).
                    Farmer Details: Age {meta['age']}, Sector {meta['sector']}.
                    User asked: "{prompt}"
                    
                    Explain this result professionally and give one tip. 
                    Keep it conversational but grounded in the data.
                    """

                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[
                            {"role": "system", "content": "You are an expert Agricultural Credit Officer."},
                            {"role": "user", "content": ai_prompt}
                        ]
                        max_tokens=500
                    )
                    
                    full_reply = response.choices[0].message.content
                    st.markdown(full_reply)
                    st.session_state.messages.append({"role": "assistant", "content": full_reply})

                except Exception as e:
                    st.error(f"Error connecting to Featherless.ai: {e}")


