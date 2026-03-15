import streamlit as st
from openai import OpenAI
import joblib

def render():
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    current_lang = st.session_state.get('lang', 'English')
    st.markdown(f"<h1 style='color: #2E7D32;'>🤖 AI Chatbot ({current_lang})</h1>", unsafe_allow_html=True)

    # --- Sync Notification: Validating the "Farmer Profile First" logic ---
    if "last_profile" in st.session_state:
        p = st.session_state.last_profile
        with st.container(border=True):
            st.success(f"✅ **{current_lang} Notification:**")
            st.write(f"I am synchronized with your **Farmer Profile** (Age: {p['age']}, Sector: {p['sector']}).")
    else:
        st.warning("⚠️ **Farmer Profile Required:** Please complete the 'Farmer Profile' section first so I can analyze your specific data.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask me about your credit analysis...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing profile..."):
                try:
                    profile_info = st.session_state.get("last_profile", "User hasn't filled a profile yet.")
                    system_instructions = f"Context: {profile_info}. Language: {current_lang}. Be a helpful agri-finance assistant."

                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[{"role": "system", "content": system_instructions}, {"role": "user", "content": prompt}]
                    )
                    
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #2E7D32;'>🌾 <strong>Farm Ledger Africa</strong> | Hybrid AI Engine</div>", unsafe_allow_html=True)
