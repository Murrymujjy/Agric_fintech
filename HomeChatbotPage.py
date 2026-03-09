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

    # --- Context Sync Notification ---
    if "last_profile" in st.session_state:
        p = st.session_state.last_profile
        with st.container(border=True):
            st.success(f"✅ **{current_lang} Notification:**")
            st.write(f"I am synchronized with the profile for the **{p['age']}-year-old farmer** from the **{p['sector']}** sector. My analysis is based on your **{p['prediction']}** status.")
    else:
        st.warning("⚠️ Please complete your **Farmer Profile** first for personalized credit analysis.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("Ask about your credit score...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    profile_info = st.session_state.get("last_profile", "No specific profile loaded yet.")
                    system_instructions = f"""
                    You are a financial inclusion assistant. 
                    Context: {profile_info}
                    Language: {current_lang}
                    Answer based on the specific farmer profile details provided.
                    """

                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[
                            {"role": "system", "content": system_instructions},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500
                    )
                    
                    reply = response.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})

                except Exception as e:
                    st.error(f"Error: {e}")

    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #2E7D32;'>🌾 <strong>Farm Ledger Africa</strong> | Powered by AI ({current_lang})</div>", unsafe_allow_html=True)
