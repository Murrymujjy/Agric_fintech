import streamlit as st
import numpy as np
import joblib
from streamlit_extras.let_it_rain import rain
from streamlit_extras.badges import badge

def render():
    # Load models
    models = {
        "Logistic Regression": joblib.load("models_logistic_regression_model.pkl"),
        "Decision Tree": joblib.load("models_decision_tree_model.pkl")
    }

    st.set_page_config(page_title="Farmer Credit Scoring", page_icon="🌾", layout="centered")

    st.markdown("""
        <style>
        .main {
            background-color: #f4f9f4;
            padding: 20px;
            border-radius: 10px;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("📋 Farmer Credit Profile & Scoring")
    st.markdown("Fill in the farmer’s information to check their **creditworthiness** and see **how different models rate them.**")

    # Model selector
    selected_model = st.selectbox("🔍 Select Prediction Model", list(models.keys()))

    # Explanation for model
    with st.expander("📘 What do these models mean?"):
        st.markdown("""
        - **Logistic Regression**: A statistical model that predicts the probability of a binary outcome (like yes/no for loan).
        - **Decision Tree**: A tree-like structure that breaks down data decisions based on features.
        """)

    # Education mapping
    education_mapping = {
        'NONE': 0, 'NURSERY': 0,
        'QUARANIC/INTEGRATED QUARANIC': 1, 'OTHER RELIGIOUS': 1,
        'PRIMARY': 2, 'ADULT EDUCATION': 2,
        'JUNIOR SECONDARY': 3, 'MODERN SCHOOL': 3, 'LOWER/UPPER 6': 3,
        'SENIOR SECONDARY': 4, 'SECONDARY VOCATIONAL/TECHNICAL/COMMERCIAL': 4,
        'TEACHER TRAINING': 5, 'TERTIARY VOCATIONAL/TECHNICAL/COMMERCIAL': 5,
        'POLYTECHNIC/PROF': 6, 'NATIONAL CERTIFICATE OF EDUCATION (NCE)': 6,
        '1st DEGREE': 6, 'HIGHER DEGREE (POST-GRADUATE)': 7,
        'OTHER': 8
    }

    sector_map = {"Urban": 0, "Rural": 1}

    # Input form
    with st.form("farmer_form"):
        age = st.slider("Age", 18, 60, 30)
        years = st.slider("Years in Community", 0, 40, 5)
        education = st.selectbox("Level of Education", list(education_mapping.keys()))
        phone = st.radio("Has Access to Phone?", ["Yes", "No"])
        sector = st.selectbox("Urban or Rural Sector", ["Rural", "Urban"])
        women_access = st.radio("Has Access to Women's Support?", ["Yes", "No"])
        submit = st.form_submit_button("🔍 Predict Creditworthiness")

    if submit:
        education_encoded = education_mapping.get(education, 8)
        phone_encoded = 1 if phone == "Yes" else 0
        sector_encoded = sector_map[sector]
        women_encoded = 1 if women_access == "Yes" else 0

        X = np.array([[age, years, education_encoded, phone_encoded, sector_encoded, women_encoded]])
        model = models[selected_model]
        prediction = model.predict(X)[0]

        st.subheader("🧾 Prediction Result")
        if prediction == 1:
            st.success("✅ This farmer is likely to get a loan!")
            rain(emoji="💰", font_size=40, falling_speed=3, animation_length="infinite")
        else:
            st.error("⚠️ This farmer is considered high risk.")

        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(X)[0][1]
            st.info(f"📊 Confidence Score (probability of approval): **{prob:.2f}**")

        st.markdown("---")
        st.markdown("### 🔑 Tips to Improve Credit Score")
        st.markdown("""
        - Stay longer in your community  
        - Complete at least secondary education  
        - Maintain phone access for communication  
        - Join cooperative or women-focused support groups  
        """)

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)

