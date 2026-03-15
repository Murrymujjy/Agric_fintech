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
            "profile": "Farmer Profile", "voice": "Voice Assistant", "chat": "AI Chatbot", "lender": "Lender Dashboard"
        },
        "Luganda (Uganda)": {
            "welcome": "Kulaba ku Farm Ledger Africa",
            "mission": "Okusobozesa abalimi abato okufuna amagezi n'obuyambi mu by'ensimbi nga tukozesa amagezi ga AI mu nnimi ez'enjawulo.",
            "sub": "Londako wamanga okutandika:",
            "profile": "Ebikwata ku mulimi", "voice": "Okukozesa eddoboozi", "chat": "Chatbot y'amagezi", "lender": "Ebirowoozo by'abawozi"
        },
        "Yoruba (Nigeria)": {
            "welcome": "Ẹ kú àbọ̀ sí Farm Ledger Africa",
            "mission": "Fífún àwọn àgbẹ̀ ní agbára láti rí àwìn pẹ̀lú ìmọ̀ ẹ̀rọ AI àti àwọn ohun èlò ìṣúnná owó ní èdè abínibí wọn.",
            "sub": "Yan ohun èlò kan láti bẹ̀rẹ̀:",
            "profile": "Ìròyìn Àgbẹ̀", "voice": "Olùrànlọ́wọ́ Ohùn", "chat": "AI Chatbot", "lender": "Dashboard Ayínilò"
        }
    }
    return translations.get(lang, translations["English"])

def main():
    st.set_page_config(page_title="Farm Ledger Africa", page_icon="🌾", layout="wide")

    if "lang" not in st.session_state:
        st.session_state.lang = "English"
    if "selected_nav" not in st.session_state:
        st.session_state.selected_nav = "🏠 Home"

    with st.sidebar:
        st.title("🌍 Language / Olulimi")
        st.session_state.lang = st.selectbox("Global Language Setting:", 
            ["English", "Luganda (Uganda)", "Yoruba (Nigeria)", "Hausa (Nigeria)", "Igbo (Nigeria)", 
             "Swahili (East Africa)", "Zulu (South Africa)", "Amharic (Ethiopia)", "Wolof (Senegal)", "Afrikaans (South Africa)"])
        
        st.markdown("---")
        # --- REORDERED NAV OPTIONS ---
        nav_options = ["🏠 Home", "📋 Farmer Profile", "🎙️ Voice Assistant", "🤖 Chatbot", "📊 Lender Dashboard", "📈 Insights"]
        
        selected = option_menu(
            "Main Menu", nav_options,
            icons=["house", "person-badge", "mic", "robot", "speedometer2", "graph-up"],
            menu_icon="cast", 
            default_index=nav_options.index(st.session_state.selected_nav),
            styles={
                "icon": {"color": "#2E7D32"}, 
                "nav-link-selected": {"background-color": "#2E7D32"},
            }
        )
        st.session_state.selected_nav = selected

    t = get_translations(st.session_state.lang)

    if st.session_state.selected_nav == "🏠 Home":
        st.markdown(f"<h1 style='color: #2E7D32;'>🚜 {t['welcome']}</h1>", unsafe_allow_html=True)
        st.markdown(f"**{t['mission']}**")
        st.markdown(f"### {t['sub']}")

        # --- REORDERED DASHBOARD COLUMNS ---
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.subheader(f"📋 {t['profile']}")
                st.write("Start here: Enter your details to calculate your credit score.")
                if st.button(f"Go to {t['profile']} ➔", key="btn_profile"):
                    st.session_state.selected_nav = "📋 Farmer Profile"; st.rerun()

            with st.container(border=True):
                st.subheader(f"🤖 {t['chat']}")
                st.write("Get AI-powered explanations of your results.")
                if st.button(f"Open {t['chat']} ➔", key="btn_chat"):
                    st.session_state.selected_nav = "🤖 Chatbot"; st.rerun()

        with col2:
            with st.container(border=True):
                st.subheader(f"🎙️ {t['voice']}")
                st.write("Apply using your voice in your native language.")
                if st.button(f"Start {t['voice']} ➔", key="btn_voice"):
                    st.session_state.selected_nav = "🎙️ Voice Assistant"; st.rerun()

            with st.container(border=True):
                st.subheader(f"📊 {t['lender']}")
                st.write("Management hub for financial institutions.")
                if st.button(f"Open {t['lender']} ➔", key="btn_lender"):
                    st.session_state.selected_nav = "📊 Lender Dashboard"; st.rerun()

    # ---- Page Routing ----
    elif st.session_state.selected_nav == "📋 Farmer Profile":
        farm_profile.render()
    elif st.session_state.selected_nav == "🎙️ Voice Assistant":
        voice_assistant.render()
    elif st.session_state.selected_nav == "🤖 Chatbot":
        HomeChatbotPage.render()
    elif st.session_state.selected_nav == "📊 Lender Dashboard":
        lender_dashboard.render()
    elif st.session_state.selected_nav == "📈 Insights":
        insights.render()

if __name__ == "__main__":
    main()
