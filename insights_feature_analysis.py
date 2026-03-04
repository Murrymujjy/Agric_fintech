import streamlit as st
import pandas as pd
import plotly.express as px

powerbi_url = "https://app.fabric.microsoft.com/view?r=eyJrIjoiNTlhYTAwMDgtZGVkOS00NTEzLWE0ZjktMzM4Y2Y5ZWE2MTg0IiwidCI6Ijg4ZTlhN2RjLTU2MzMtNGM2Ni1iNjZjLTkyZGY1Y2E3NDhmYyJ9"

def render():
    st.title("📈 Insights & Visualizations")

    # Embed Power BI dashboard
    st.markdown("### 🧠 Power BI Dashboard")
    st.components.v1.iframe(powerbi_url, height=800, width=1200)

    # Upload CSV for additional visualizations
    st.markdown("### 📂 Upload Prediction Data (CSV)")
    uploaded_file = st.file_uploader("Upload the prediction results (e.g. credit_predictions.csv)", type="csv")

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        # Check for required columns
        if 'Loan Approved (1=Yes)' in df.columns and 'Confidence Score' in df.columns:
            st.markdown("### 📊 Loan Approval by Education Level")
            fig1 = px.histogram(df, x="level_of_education", color="Loan Approved (1=Yes)",
                                barmode="group", title="Approval by Education Level")
            st.plotly_chart(fig1, use_container_width=True)

            st.markdown("### 📞 Approval Confidence by Phone Access")
            if 'phone_access' in df.columns:
                fig2 = px.box(df, x="phone_access", y="Confidence Score", color="Loan Approved (1=Yes)",
                             title="Confidence Score vs Phone Access")
                st.plotly_chart(fig2, use_container_width=True)

            st.markdown("### 🌍 Approval by Sector")
            if 'sector' in df.columns:
                fig3 = px.histogram(df, x="sector", color="Loan Approved (1=Yes)", barmode="group",
                                    title="Approval by Sector")
                st.plotly_chart(fig3, use_container_width=True)

            st.markdown("### 📉 Confidence Score Distribution")
            fig4 = px.histogram(df, x="Confidence Score", nbins=20, title="Distribution of Confidence Scores")
            st.plotly_chart(fig4, use_container_width=True)
        else:
            st.warning("Required columns not found in uploaded data. Please upload a valid prediction CSV file.")
    else:
        st.info("Upload a CSV file to see dynamic charts.")

    st.markdown("---")
    st.markdown("<div style='text-align: center;'>📌 Made with ❤️ by <strong>Farm Ledger</strong></div>", unsafe_allow_html=True)

