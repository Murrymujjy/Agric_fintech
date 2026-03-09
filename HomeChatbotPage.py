import streamlit as st
import joblib
import numpy as np
import re
from openai import OpenAI

def render():
    # 1. Setup API Client
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    # 2. Load the Decision Engine [cite: 2026-03-02]
    try:
        model = joblib.load("models_logistic_regression_model.pkl")
    except Exception:
        st.error("Decision model not found. Please upload models_logistic_regression_model.pkl")
        return

    # 3. Dynamic UI based on Global Language
    current_lang = st.session_state.lang
    st.title(f"🤖 AI Chatbot ({current_lang})")
    st.markdown(f"I can analyze creditworthiness and explain it in **{current_lang}**.")

    # Chat History Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # --- Input Processing ---
    prompt = st.chat_input("Ex: A 35 year old farmer in a rural area...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # A. Use LLM to extract numerical data from text
                    # This handles varied phrasing across different languages
                    extract_prompt = f"""
                    Extract 6 features from: "{prompt}". 
                    Format: [Age, YearsInCommunity, Education(0-8), HasPhone(0/1), Rural(1)/Urban(0), WomenSupport(0/1)]
                    Return ONLY the list. Example: [35, 10, 4, 1, 1, 0]
                    """
                    
                    extraction = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[{"role": "user", "content": extract_prompt}],
                        max_tokens=100
                    )
                    
                    data_list = eval(extraction.choices[0].message.content.strip().strip('`'))
                    X = np.array([data_list])

                    # B. Perform Mathematical Credit Scoring [cite: 2026-03-02]
                    prediction = model.predict(X)[0]
                    prob = model.predict_proba(X)[0][1]

                    # C. Generate Explanation in Selected Language
                    explain_prompt = f"""
                    User Question: "{prompt}"
                    Decision: {'Approved' if prediction == 1 else 'High Risk'}
                    Confidence: {prob:.2f}
                    
                    Translate the decision into {current_lang} and provide a 2-sentence 
                    explanation in {current_lang} about why this was the result.
                    """
                    
                    explanation = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[{"role": "user", "content": explain_prompt}],
                        max_tokens=500
                    )
                    
                    final_reply = explanation.choices[0].message.content
                    st.markdown(final_reply)
                    st.session_state.messages.append({"role": "assistant", "content": final_reply})

                except Exception as e:
                    st.error(f"Error: {e}. Please try again.")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center;'>📌 Multi-Lingual AI Engine | <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)
