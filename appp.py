import streamlit as st
from streamlit_option_menu import option_menu
import HomeChatbotPage
import farm_profile
import lender_dashboard
import insights_feature_analysis as insights
from openai import OpenAI
import os

# --- Featherless.ai Engine Configuration ---
# This centralizes the API logic for use across the Home and Chatbot pages.
def get_ai_engine():
    if "FEATHERLESS_API_KEY" in st.secrets:
        return OpenAI(
            base_url="https://api.featherless.ai/v1",
            api_key=st.secrets["FEATHERLESS_API_KEY"]
        )
    return None

# ---- Background Style ----
def set_bg_animation():
    st.markdown("""
    <style>
    .main {
        background-color: #f0f4f8; 
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        color: white;
        background-color: #2e7d32; /* Forest Green for Agriculture theme */
        border-radius: 8px;
        width: 100%;
    }
    .sidebar .sidebar-content {
        background-image: linear-gradient(#2e7d32, #1b5e20);
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# ---- Session Setup ----
if "selected_nav" not in st.session_state:
    st.session_state.selected_nav = "🏠 Home"

# ---- Sidebar Navigation ----
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2572/2572512.png", width=100) # Optional Logo
    selected = option_menu(
        "Farm Ledger Menu",
        ["🏠 Home", "🤖 Chatbot", "📋 Farmer Credit Profile", "📊 Lender Dashboard", "📈 Insights", "💡 About the AI"],
        icons=["house", "robot", "person-badge", "speedometer2", "graph-up", "info-circle"],
        menu_icon="cast",
        default_index=0
    )
    st.session_state.selected_nav = selected
    
    st.sidebar.markdown("---")
    st.sidebar.write("🟢 **System Status: Online**")
    st.sidebar.write("API: Featherless.ai (Llama 3.1)")

set_bg_animation()

# ---- Home Page ----
if st.session_state.selected_nav == "🏠 Home":
    st.title("🌾 Farm Ledger: Hybrid AI Credit Scoring")
    st.markdown(
        """
        ### Transforming Rural Finance with Explainable AI
        Welcome to **Farm Ledger**, a production-grade platform that combines **Machine Learning** with 
        **Generative AI** to make credit scoring fair, fast, and transparent.
        
        **What would you like to do today?**
        """, unsafe_allow_html=True
    )

    # Grid Layout for Navigation
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.subheader("🤖 AI Chatbot")
            st.write("Talk to our AI assistant to analyze specific farmer profiles using natural language.")
            if st.button("Launch Chatbot"):
                st.session_state.selected_nav = "🤖 Chatbot"
                st.rerun()

        st.subheader("📊 Lender Hub")
        st.write("Process bulk CSV files and generate instant credit approvals for hundreds of farmers.")
        if st.button("Open Lender Dashboard"):
            st.session_state.selected_nav = "📊 Lender Dashboard"
            st.rerun()

    with col2:
        st.subheader("📋 Credit Profiling")
        st.write("Manually enter farmer data to see how different ML models (Logistic vs Tree) rank them.")
        if st.button("Go to Profiler"):
            st.session_state.selected_nav = "📋 Farmer Credit Profile"
            st.rerun()

        st.subheader("📈 Insights")
        st.write("Visualize demographic trends and approval rates across urban and rural sectors.")
        if st.button("View Analysis"):
            st.session_state.selected_nav = "📈 Insights"
            st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Developed for the 2026 AI Innovation Hackathon | <strong>Farm Ledger Team</strong></div>", unsafe_allow_html=True)

# ---- About the AI Page (New Subsection) ----
elif st.session_state.selected_nav == "💡 About the AI":
    st.title("💡 The Hybrid AI Architecture")
    st.markdown("""
    This project utilizes a **Two-Tiered AI Stack** to solve the 'Black Box' problem in financial services.
    """)

    

    st.write("### 1. The Decision Engine (Scikit-Learn)")
    st.write("""
    We use **Logistic Regression** and **Decision Trees** for the actual scoring. 
    These models were trained on Nigerian agricultural demographic data. 
    They provide the *Probability Score*.
    """)

    st.write("### 2. The Explanation Layer (Featherless.ai)")
    st.write("""
    Raw scores are passed to **Featherless.ai** (Meta-Llama-3.1-8B-Instruct). 
    The API analyzes the feature importance and generates a **Natural Language Explanation** so farmers know exactly how to improve their scores.
    """)
    
    st.success("**Why Featherless?** It allows us to run state-of-the-art LLMs via serverless API, making our app lightweight and scalable for rural deployment.")

# ---- Page Routing ----
elif st.session_state.selected_nav == "🤖 Chatbot":
    HomeChatbotPage.render()

elif st.session_state.selected_nav == "📋 Farmer Credit Profile":
    farm_profile.render()

elif st.session_state.selected_nav == "📊 Lender Dashboard":
    lender_dashboard.render()

elif st.session_state.selected_nav == "📈 Insights":
    insights.render()
