import streamlit as st
import pandas as pd
import joblib

def render():
    st.title("📊 Lender Dashboard - Batch Credit Scoring")
    st.markdown("""
    Upload a CSV file containing farmer data to get creditworthiness predictions in bulk.  
    Make sure your CSV includes the following columns:
    - `age`: Age of the farmer
    - `years_in_community`: Years the farmer has lived in the community
    - `education_level`: Encoded education level (0–8)
    - `has_phone`: 1 if the farmer has phone access, else 0
    - `sector`: 1 for rural, 0 for urban
    - `women_access_support`: 1 if woman with access to support, else 0
    """)

    # --- Download Sample CSV ---
    sample_data = pd.DataFrame({
        "age": [35, 42],
        "years_in_community": [10, 7],
        "education_level": [4, 6],
        "has_phone": [1, 0],
        "sector": [1, 0],
        "women_access_support": [1, 0]
    })

    csv = sample_data.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Sample CSV",
        data=csv,
        file_name="sample_farmers.csv",
        mime="text/csv",
        help="Download a sample CSV with the correct format for predictions."
    )

    # --- Upload Section ---
    uploaded_file = st.file_uploader("📤 Upload CSV file", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            st.write("🔍 Uploaded Data Preview:")
            st.dataframe(df)

            required_columns = {"age", "years_in_community", "education_level", "has_phone", "sector", "women_access_support"}
            if not required_columns.issubset(df.columns):
                missing = required_columns - set(df.columns)
                st.error(f"❌ Missing required columns: {', '.join(missing)}")
                return

            model = joblib.load("models_logistic_regression_model.pkl")
            predictions = model.predict(df)
            probabilities = model.predict_proba(df)[:, 1]

            df["Prediction"] = ["✅ Approved" if p == 1 else "❌ Declined" for p in predictions]
            df["Confidence"] = [f"{prob:.2f}" for prob in probabilities]

            st.success("🎯 Predictions Generated Successfully!")
            st.write(df)

            result_csv = df.to_csv(index=False).encode("utf-8")
            st.download_button("⬇️ Download Results as CSV", result_csv, file_name="credit_predictions.csv", mime="text/csv")

        except Exception as e:
            st.error("⚠️ Failed to process the uploaded file. Please make sure it matches the sample format.")
            st.exception(e)
