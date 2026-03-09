import streamlit as st
from streamlit_option_menu import option_menu
import HomeChatbotPage
import farm_profile
import lender_dashboard
import insights_feature_analysis as insights
import voice_assistant 

# --- Global Translation Engine ---
def get_translations(lang):
    translations = {
        "English": {
            "welcome": "Welcome to Farm Ledger Africa",
            "mission": "Empowering unbanked smallholder farmers with AI-driven credit scoring and multi-lingual financial inclusion tools.",
            "sub": "Select a feature to begin:",
            "chat": "AI Chatbot", "voice": "Voice Assistant", "profile": "Farmer Profile", "lender": "Lender Dashboard"
        },
        "Luganda (Uganda)": {
            "welcome": "Kulaba ku Farm Ledger Africa",
            "mission": "Okusobozesa abalimi abato okufuna amagezi n'obuyambi mu by'ensimbi nga tukozesa amagezi ga AI mu nnimi ez'enjawulo.",
            "sub": "Londako wamanga okutandika:",
            "chat": "Chatbot y'amagezi", "voice": "Okukozesa eddoboozi", "profile": "Ebikwata ku mulimi", "lender": "Ebirowoozo by'abawozi"
        },
        "Yoruba (Nigeria)": {
            "welcome": "Ẹ kú àbọ̀ sí Farm Ledger Africa",
            "mission": "Fífún àwọn àgbẹ̀ ní agbára láti rí àwìn pẹ̀lú ìmọ̀ ẹ̀rọ AI àti àwọn ohun èlò ìṣúnná owó ní èdè abínibí wọn.",
            "sub": "Yan ohun èlò kan láti bẹ̀rẹ̀:",
            "chat": "AI Chatbot", "voice": "Olùrànlọ́wọ́ Ohùn", "profile": "Ìròyìn Àgbẹ̀", "lender": "Dashboard Ayínilò"
        }
        # ... (Add other language translations as needed)
    }
    return translations.get(lang, translations["English"])

def main():
    st.set_page_config(page_title="Farm Ledger Africa", page_icon="🌾", layout="wide")

    # --- Initialization ---
    if "lang" not in st.session_state:
        st.session_state.lang = "English"
    if "selected_nav" not in st.session_state:
        st.session_state.selected_nav = "🏠 Home"

    # --- Sidebar with Green Custom Styling ---
    with st.sidebar:
        st.title("🌍 Language / Olulimi")
        st.session_state.lang = st.selectbox("Global Language Setting:", 
            ["English", "Luganda (Uganda)", "Yoruba (Nigeria)", "Hausa (Nigeria)", "Igbo (Nigeria)", 
             "Swahili (East Africa)", "Zulu (South Africa)", "Amharic (Ethiopia)", "Wolof (Senegal)", "Afrikaans (South Africa)"])
        
        st.markdown("---")
        nav_options = ["🏠 Home", "🤖 Chatbot", "🎙️ Voice Assistant", "📋 Farmer Profile", "📊 Lender Dashboard", "📈 Insights"]
        
        # Fixed Cursor Bar: Changed selection background from red to forest green
        selected = option_menu(
            "Main Menu", nav_options,
            icons=["house", "robot", "mic", "person-badge", "speedometer2", "graph-up"],
            menu_icon="cast", 
            default_index=nav_options.index(st.session_state.selected_nav),
            styles={
                "icon": {"color": "#2E7D32"}, 
                "nav-link-selected": {"background-color": "#2E7D32"}, # Green highlight
            }
        )
        st.session_state.selected_nav = selected

    t = get_translations(st.session_state.lang)

    # ---- Interactive Home Dashboard ----
    if st.session_state.selected_nav == "🏠 Home":
        st.markdown(f"<h1 style='color: #2E7D32;'>🚜 {t['welcome']}</h1>", unsafe_allow_html=True)
        # Added Project Description as requested
        st.markdown(f"**{t['mission']}**")
        st.markdown(f"### {t['sub']}")

        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader(f"🤖 {t['chat']}")
                if st.button(f"Open {t['chat']} ➔", key="btn_chat"):
                    st.session_state.selected_nav = "🤖 Chatbot"; st.rerun()

            with st.container(border=True):
                st.subheader(f"📋 {t['profile']}")
                if st.button(f"Go to {t['profile']} ➔", key="btn_profile"):
                    st.session_state.selected_nav = "📋 Farmer Profile"; st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader(f"🎙️ {t['voice']}")
                if st.button(f"Start {t['voice']} ➔", key="btn_voice"):
                    st.session_state.selected_nav = "🎙️ Voice Assistant"; st.rerun()

            with st.container(border=True):
                st.subheader(f"📊 {t['lender']}")
                if st.button(f"Open {t['lender']} ➔", key="btn_lender"):
                    st.session_state.selected_nav = "📊 Lender Dashboard"; st.rerun()

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
