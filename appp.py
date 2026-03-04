import streamlit as st
from streamlit_option_menu import option_menu
import HomeChatbotPage
import farm_profile
import lender_dashboard
import insights_feature_analysis as insights
import voice_assistant  # The new voice-to-credit module
from openai import OpenAI

# ---- Background & Theme Styling ----
def set_custom_style():
    st.markdown("""
    <style>
    .main {
        background-color: #f4f7f6;
    }
    .stButton>button {
        color: white;
        background-color: #2e7d32;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-weight: bold;
    }
    .stAudioInput {
        border: 2px solid #2e7d32;
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ---- Session State Initialization ----
if "selected_nav" not in st.session_state:
    st.session_state.selected_nav = "🏠 Home"

def main():
    set_custom_style()

    # ---- Sidebar Navigation ----
    with st.sidebar:
        st.title("🌾 Farm Ledger")
        st.markdown("---")
        selected = option_menu(
            "Navigation",
            ["🏠 Home", "🤖 Chatbot", "🎙️ Voice Assistant", "📋 Farmer Credit Profile", "📊 Lender Dashboard", "📈 Insights", "💡 About the AI"],
            icons=["house", "robot", "mic", "person-badge", "speedometer2", "graph-up", "info-circle"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "#2e7d32", "font-size": "25px"}, 
                "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
                "nav-link-selected": {"background-color": "#2e7d32"},
            }
        )
        st.session_state.selected_nav = selected
        
        st.sidebar.markdown("---")
        st.sidebar.info(f"**Backend:** Featherless.ai API\n\n**Model:** Llama 3.1 & Logistic Regression")

    # ---- Page Routing Logic ----
    if st.session_state.selected_nav == "🏠 Home":
        st.title("🚜 Farm Ledger: AI-Driven Credit Scoring")
        st.markdown("""
        ### Empowering Farmers with Explainable AI
        Welcome to the next generation of agricultural finance. **Farm Ledger** uses a hybrid approach:
        - **Precision:** Machine Learning (Logistic Regression) for data-driven approvals.
        - **Inclusion:** Voice-to-Text for accessible credit profiling.
        - **Transparency:** Featherless.ai (LLMs) to explain every financial decision.
        """)
        
        # Dashboard Shortcut Buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🎤 Try Voice Assistant"):
                st.session_state.selected_nav = "🎙️ Voice Assistant"
                st.rerun()
            if st.button("📈 View Insights"):
                st.session_state.selected_nav = "📈 Insights"
                st.rerun()
        with col2:
            if st.button("🤖 Launch Chatbot"):
                st.session_state.selected_nav = "🤖 Chatbot"
                st.rerun()
            if st.button("📊 Bulk Processing"):
                st.session_state.selected_nav = "📊 Lender Dashboard"
                st.rerun()

    elif st.session_state.selected_nav == "🎙️ Voice Assistant":
        voice_assistant.render()

    elif st.session_state.selected_nav == "🤖 Chatbot":
        HomeChatbotPage.render()

    elif st.session_state.selected_nav == "📋 Farmer Credit Profile":
        farm_profile.render()

    elif st.session_state.selected_nav == "📊 Lender Dashboard":
        lender_dashboard.render()

    elif st.session_state.selected_nav == "📈 Insights":
        insights.render()

    elif st.session_state.selected_nav == "💡 About the AI":
        st.title("💡 The Technology Behind Farm Ledger")
        
        st.subheader("1. The Decision Engine")
        st.write("""
        We utilize a **Logistic Regression** model for its transparency in high-stakes financial decisions. 
        It evaluates features like education, community tenure, and phone access to predict loan repayment 
        probability with mathematical precision.
        """)

        st.subheader("2. The Reasoning Layer")
        st.write("""
        Powered by **Featherless.ai**, we integrate Meta's Llama 3.1 model to perform:
        - **Feature Extraction:** Converting raw voice recordings into structured data.
        - **Natural Language Explanations:** Translating complex probability scores into actionable advice.
        """)
        
        

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Built for the 2026 AI Innovation Hackathon | <strong>Farm Ledger Team</strong></div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
