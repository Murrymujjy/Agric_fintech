import streamlit as st
import joblib
import numpy as np
import re
from ai_engine import get_ai_explanation # Import our new engine

def render():
    # Load your existing logistic regression model
    model = joblib.load("models_logistic_regression_model.pkl")

    st.title("🤖 Intelligent Credit Assistant")
    st.markdown("I now use **Featherless.ai** to explain my predictions!")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! Ask me about a farmer's profile."}]

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ex: Will a 40yo farmer in a rural area get a loan?")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Consulting AI models..."):
                # 1. Parse Input (Your existing logic)
                # ... [Keep your parse_input code here] ...
                X = np.array([[30, 5, 4, 1, 1, 0]]) # Placeholder for parsed data
                
                # 2. Get Data-Driven Prediction
                prediction = model.predict(X)[0]
                prob = model.predict_proba(X)[0][1]

                # 3. Get Featherless AI Explanation
                features = {'age': 30, 'education': 'Senior Secondary', 'sector': 'Rural'}
                explanation = get_ai_explanation(prediction, prob, features)
                
                st.markdown(explanation)
                st.session_state.messages.append({"role": "assistant", "content": explanation})
