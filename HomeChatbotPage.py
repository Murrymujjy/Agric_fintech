import streamlit as st
import joblib
import numpy as np
import re

def render():  # 👈 THIS IS THE FIX
    model = joblib.load("models_logistic_regression_model.pkl")

    st.title("🤖 AI Chatbot for Farmer Credit Scoring")

    st.markdown("Ask questions like:")
    st.markdown("- *Will a 40-year-old farmer in rural area with secondary education get a loan?*")
    st.markdown("- *What is the credit score of a woman with access to phone and tertiary education?*")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi there! I'm your AI credit scoring assistant. Ask me about any farmer profile and I’ll predict their creditworthiness."}
        ]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    education_mapping = {
        'none': 0, 'nursery': 0,
        'quaranic': 1, 'other religious': 1,
        'primary': 2, 'adult education': 2,
        'junior': 3, 'modern': 3, 'lower': 3, 'upper': 3,
        'senior': 4, 'technical': 4, 'commercial': 4,
        'teacher': 5, 'tertiary vocational': 5,
        'polytechnic': 6, 'nce': 6, 'degree': 6, 'higher': 7,
        'other': 8
    }
    sector_map = {"urban": 0, "rural": 1}

    def parse_input(text):
        text = text.lower()
        age_match = re.search(r"(\d+)\s*year", text)
        age = int(age_match.group(1)) if age_match else 30
        years_lived = 5

        education_encoded = 8
        for key in education_mapping:
            if key in text:
                education_encoded = education_mapping[key]
                break

        phone = 1 if "has phone" in text or "access to phone" in text else 0
        sector_encoded = 1 if "rural" in text else 0
        women_access = 1 if "woman" in text and "support" in text else 0

        return np.array([[age, years_lived, education_encoded, phone, sector_encoded, women_access]])

    prompt = st.chat_input("Type your question here...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    X = parse_input(prompt)
                    prediction = model.predict(X)[0]
                    prob = model.predict_proba(X)[0][1]

                    if prediction == 1:
                        reply = f"✅ This farmer is likely to get a loan! (Confidence: **{prob:.2f}**)"
                    else:
                        reply = f"⚠️ This farmer might be considered high risk. (Confidence: **{prob:.2f}**)"
                except Exception as e:
                    reply = "❌ Sorry, I couldn’t understand or process your request."

                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)

