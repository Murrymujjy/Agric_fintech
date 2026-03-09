import streamlit as st
from openai import OpenAI
import joblib

def render():
    # 1. API Client Setup
    client = OpenAI(
        base_url="https://api.featherless.ai/v1",
        api_key=st.secrets["FEATHERLESS_API_KEY"]
    )
    
    # 2. Page Title & Language Sync [cite: 2025-12-20, 2026-03-02]
    current_lang = st.session_state.get('lang', 'English')
    st.title(f"🤖 AI Chatbot ({current_lang})")

    # --- THE NOTIFICATION BOX ---
    # Notifies the user that the Chatbot is using their Profile data [cite: 2026-03-02]
    if "last_profile" in st.session_state:
        p = st.session_state.last_profile
        # Using a green-bordered container for brand consistency
        with st.container(border=True):
            st.success(f"✅ **{current_lang} Notification:**")
            st.write(f"""
            This chatbot is currently synchronized with your **Farmer Profile**. 
            It is analyzing your specific data (Age: {p['age']}, Sector: {p['sector']}) 
            to explain why the model gave you a status of **{p['prediction']}**.
            """)
    else:
        st.warning("⚠️ **Note:** To get personalized explanations, please complete your **Farmer Profile** first.")

    # 3. Chat History Setup
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # 4. Input Processing with Context
    prompt = st.chat_input("Ask me anything about your credit result...")

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing profile context..."):
                try:
                    # Injecting the profile data into the system prompt
                    profile_info = ""
                    if "last_profile" in st.session_state:
                        profile_info = f"The user's profile details are: {st.session_state.last_profile}."

                    system_instructions = f"""
                    You are a financial inclusion assistant for African farmers.
                    Context: {profile_info}
                    Response Language: {current_lang}
                    Goal: Explain the credit status clearly based on the provided profile details.
                    """

                    response = client.chat.completions.create(
                        model="meta-llama/Meta-Llama-3.1-8B-Instruct",
                        messages=[
                            {"role": "system", "content": system_instructions},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500
                    )
                    
                    final_text = response.choices[0].message.content
                    st.markdown(final_text)
                    st.session_state.messages.append({"role": "assistant", "content": final_text})

                except Exception as e:
                    st.error(f"Error connecting to AI: {e}")

    # Footer with Green Branding
    st.markdown("---")
    st.markdown(f"<div style='text-align: center; color: #2E7D32;'>🌍 Powered by <strong>Farm Ledger Africa</strong> in {current_lang}</div>", unsafe_allow_html=True)
