import os
from openai import OpenAI
import streamlit as st

# Setup client - Featherless is OpenAI compatible
client = OpenAI(
    base_url="https://api.featherless.ai/v1",
    api_key=st.secrets["FEATHERLESS_API_KEY"] # Store your key in secrets.toml
)

def get_ai_explanation(prediction, confidence, features):
    """Generates a human-friendly explanation of the credit score."""
    status = "Approved" if prediction == 1 else "High Risk/Declined"
    
    prompt = f"""
    A farmer profile was analyzed for a loan.
    Status: {status}
    Confidence: {confidence:.2f}
    Details: Age {features['age']}, Education level {features['education']}, Sector {features['sector']}.
    
    Act as a friendly financial advisor. Briefly explain why this farmer was {status.lower()} 
    and give one specific tip for improvement. Keep it under 60 words.
    """
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3.1-8B-Instruct", # Or any Featherless model
            messages=[{"role": "system", "content": "You are a helpful agricultural credit expert."},
                      {"role": "user", "content": prompt}],
            max_tokens=150
        )
        return response.choices[0].message.content
    except Exception as e:
        return "The AI explainer is currently offline, but your data-driven prediction is ready above."
