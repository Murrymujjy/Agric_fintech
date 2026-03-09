import streamlit as st
from streamlit_option_menu import option_menu
import HomeChatbotPage
import farm_profile
import lender_dashboard
import insights_feature_analysis as insights
import voice_assistant 

# --- Global Configuration & Translation ---
def get_translations(lang):
    translations = {
        "English": {"welcome": "Welcome to Farm Ledger Africa", "sub": "Select a feature to begin:", "chat": "AI Chatbot", "voice": "Voice Assistant", "profile": "Farmer Profile", "lender": "Lender Dashboard"},
        "Luganda (Uganda)": {"welcome": "Kulaba ku Farm Ledger Africa", "sub": "Londako wamanga okutandika:", "chat": "Chatbot y'amagezi", "voice": "Okukozesa eddoboozi", "profile": "Ebikwata ku mulimi", "lender": "Ebirowoozo by'abawozi"},
        "Yoruba (Nigeria)": {"welcome": "Ẹ kú àbọ̀ sí Farm Ledger Africa", "sub": "Yan ohun èlò kan láti bẹ̀rẹ̀:", "chat": "AI Chatbot", "voice": "Olùrànlọ́wọ́ Ohùn", "profile": "Ìròyìn Àgbẹ̀", "lender": "Dashboard Ayínilò"},
    }
    return translations.get(lang, translations["English"])

def main():
    st.set_page_config(page_title="Farm Ledger Africa", page_icon="🌾", layout="wide")

    # --- Language Selection (Global State) ---
    if "lang" not in st.session_state:
        st.session_state.lang = "English"
    if "selected_nav" not in st.session_state:
        st.session_state.selected_nav = "🏠 Home"

    with st.sidebar:
        st.title("🌍 Global Settings")
        st.session_state.lang = st.selectbox("Choose Language / Londako Olulimi:", 
            ["English", "Luganda (Uganda)", "Yoruba (Nigeria)", "Hausa (Nigeria)", "Swahili (East Africa)"])
        
        st.markdown("---")
        selected = option_menu(
            "Main Menu",
            ["🏠 Home", "🤖 Chatbot", "🎙️ Voice Assistant", "📋 Farmer Profile", "📊 Lender Dashboard", "📈 Insights"],
            icons=["house", "robot", "mic", "person-badge", "speedometer2", "graph-up"],
            menu_icon="cast", 
            default_index=0
        )
        st.session_state.selected_nav = selected

    t = get_translations(st.session_state.lang)

    # ---- Clickable Interactive Home Page ----
    if st.session_state.selected_nav == "🏠 Home":
        st.title(f"🚜 {t['welcome']}")
        st.markdown(f"### {t['sub']}")

        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader(f"🤖 {t['chat']}")
                st.write("Analyze profiles via text chat.")
                if st.button("Open Chatbot ➔", key="btn_chat"):
                    st.session_state.selected_nav = "🤖 Chatbot"
                    st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader(f"🎙️ {t['voice']}")
                st.write("Use your voice to apply for credit.")
                if st.button("Start Voice Entry ➔", key="btn_voice"):
                    st.session_state.selected_nav = "🎙️ Voice Assistant"
                    st.rerun()

        col3, col4 = st.columns(2)
        with col3:
            with st.container(border=True):
                st.subheader(f"📋 {t['profile']}")
                st.write("Manual entry for detailed credit scoring.")
                if st.button("Go to Profiler ➔", key="btn_profile"):
                    st.session_state.selected_nav = "📋 Farmer Profile"
                    st.rerun()

        with col4:
            with st.container(border=True):
                st.subheader(f"📊 {t['lender']}")
                st.write("Bulk processing for institutions.")
                if st.button("Open Dashboard ➔", key="btn_lender"):
                    st.session_state.selected_nav = "📊 Lender Dashboard"
                    st.rerun()

    # ---- Page Routing ----
    elif st.session_state.selected_nav == "🎙️ Voice Assistant":
        voice_assistant.render()
    elif st.session_state.selected_nav == "🤖 Chatbot":
        HomeChatbotPage.render()
    elif st.session_state.selected_nav == "📋 Farmer Profile":
        farm_profile.render()
    elif st.session_state.selected_nav == "📊 Lender Dashboard":
        lender_dashboard.render()
    elif st.session_state.selected_nav == "📈 Insights":
        insights.render()

if __name__ == "__main__":
    main()
