import streamlit as st
from streamlit_option_menu import option_menu
import HomeChatbotPage
import farm_profile
import lender_dashboard
import insights_feature_analysis as insights

# ---- Background Style ----
def set_bg_animation():
    st.markdown("""
    <style>
    .main {
        background-color: #e6f0ff;  /* Light blue */
        padding: 20px;
        border-radius: 10px;
    }
    .stButton>button {
        color: white;
        background-color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

set_bg_animation()

# ---- Session Setup ----
if "selected_nav" not in st.session_state:
    st.session_state.selected_nav = "🏠 Home"

# ---- Sidebar Navigation ----
with st.sidebar:
    selected = option_menu(
        "Navigation",
        ["🏠 Home", "🤖 Chatbot", "📋 Farmer Credit Profile", "📊 Lender Dashboard", "📈 Insights & Visualizations"],
        icons=["house", "robot", "file-earmark-text", "bar-chart-line", "graph-up"],
        default_index=["🏠 Home", "🤖 Chatbot", "📋 Farmer Credit Profile", "📊 Lender Dashboard", "📈 Insights & Visualizations"].index(st.session_state.selected_nav)
    )
    st.session_state.selected_nav = selected

# ---- Home Page ----
if st.session_state.selected_nav == "🏠 Home":
    st.title("🌾 Farmers Creditworthiness Platform")
    st.markdown(
        """
        <div style='font-size:15px'>
        Welcome to <b>Farmers Credit Scoring App</b>, your intelligent tool for evaluating loan eligibility of farmers.<br>
        Built with 💡 machine learning, this platform supports both <b>farmers</b> and <b>lenders</b> in making data-driven decisions.
        </div>
        <hr>
        """, unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🤖 Chatbot")
        if st.button("Go to Chatbot"):
            st.session_state.selected_nav = "🤖 Chatbot"
            st.rerun()
    with col2:
        st.markdown("### 📋 Farmer Profile")
        if st.button("Go to Farmer Profile"):
            st.session_state.selected_nav = "📋 Farmer Credit Profile"
            st.rerun()

    col3, col4 = st.columns(2)
    with col3:
        st.markdown("### 📊 Lender Dashboard")
        if st.button("Go to Lender Dashboard"):
            st.session_state.selected_nav = "📊 Lender Dashboard"
            st.rerun()
    with col4:
        st.markdown("### 📈 Insights & Analysis")
        if st.button("Go to Insights & Visualizations"):
            st.session_state.selected_nav = "📈 Insights & Visualizations"
            st.rerun()

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)

# ---- Pages ----
elif st.session_state.selected_nav == "🤖 Chatbot":
    HomeChatbotPage.render()

elif st.session_state.selected_nav == "📋 Farmer Credit Profile":
    farm_profile.render()

elif st.session_state.selected_nav == "📊 Lender Dashboard":
    lender_dashboard.render()

elif st.session_state.selected_nav == "📈 Insights & Visualizations":
    insights.render()

