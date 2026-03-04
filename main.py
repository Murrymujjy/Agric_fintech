# main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import re
import numpy as np
import io

# --- Pydantic Models (Data Shapes) ---

class FarmerData(BaseModel):
    age: int
    years_lived_in_community: int
    level_of_education: int
    phone_access: int
    sector: int
    women_access: int

class ChatbotQuery(BaseModel):
    prompt: str

# --- Chatbot Helper Functions ---

education_mapping = {
    'none': 0, 'nursery': 0,
    'quaranic': 1, 'other religious': 1,
    'primary': 2, 'adult education': 2,
    'junior': 3, 'modern': 3, 'lower': 3, 'upper': 3,
    'senior': 4, 'technical': 4, 'commercial': 4,
    'teacher': 5, 'tertiary vocational': 5,
    'polytechnic': 6, 'nce': 6, 'degree': 6, 'higher': 7,
    'other': 8
}

# --- THIS FUNCTION IS NOW SMARTER ---
def parse_input_for_chatbot(text: str):
    text = text.lower()
    
    # --- 1. Check for any relevant keywords ---
    found_age = re.search(r"(\d+)\s*year", text)
    found_education = any(key in text for key in education_mapping)
    found_phone = "phone" in text
    found_sector = "rural" in text or "urban" in text
    found_woman = "woman" in text

    # --- 2. If no keywords are found, it's not a valid query ---
    # We raise an error that our endpoint will catch.
    if not (found_age or found_education or found_phone or found_sector or found_woman):
        raise ValueError("No relevant farmer details found in query.")
    
    # --- 3. If keywords ARE found, proceed with parsing ---
    age = int(found_age.group(1)) if found_age else 30 # Default age 30
    years_lived = 5 # Default
    
    education_encoded = 8 # Default
    if found_education:
        for key in education_mapping:
            if key in text:
                education_encoded = education_mapping[key]
                break
            
    phone = 1 if found_phone else 0
    sector_encoded = 1 if "rural" in text else 0 # Defaults to 0 (urban)
    women_access = 1 if found_woman else 0
    
    return np.array([[age, years_lived, education_encoded, phone, sector_encoded, women_access]])


# --- App Setup ---

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("models_logistic_regression_model.pkl")

# --- API Endpoints (The "Phone Numbers") ---

@app.post("/predict_farmer")
async def predict_credit_score(data: FarmerData):
    # (This endpoint is unchanged)
    input_data = pd.DataFrame([data.dict()])
    prediction_raw = model.predict(input_data)[0]
    probability_raw = model.predict_proba(input_data)[0][1]
    return {
        "prediction": int(prediction_raw),
        "probability": float(probability_raw)
    }

# --- THIS ENDPOINT IS NOW SMARTER ---
@app.post("/predict_chatbot")
async def predict_from_chatbot(query: ChatbotQuery):
    try:
        # 1. Parse the text into features
        X = parse_input_for_chatbot(query.prompt)
        
        # 2. Make prediction
        prediction_raw = model.predict(X)[0]
        probability_raw = model.predict_proba(X)[0][1]
        
        # 3. Create a reply
        if prediction_raw == 1:
            reply = f"✅ This farmer is likely to get a loan! (Confidence: {probability_raw:.2f})"
        else:
            reply = f"⚠️ This farmer might be considered high risk. (Confidence: {probability_raw:.2f})"
            
        return {"reply": reply}

    # --- 4. CATCH THE ERROR WE CREATED ---
    except ValueError as e:
        # This catches our "No relevant farmer details" error
        return {"reply": "I'm not sure how to answer that. Please ask me about a farmer's profile, like 'Will a 40-year-old farmer get a loan?'"}
    except Exception as e:
        # This catches any other unexpected errors
        return {"reply": "❌ Sorry, I couldn’t understand that request."}

@app.post("/predict_batch")
async def predict_batch(file: UploadFile = File(...)):
    # (This endpoint is unchanged)
    contents = await file.read()
    data_stream = io.StringIO(contents.decode('utf-8'))
    df = pd.read_csv(data_stream)

    required_columns = [
        'age', 'years_lived_in_community', 'level_of_education', 
        'phone_access', 'sector', 'women_access'
    ]
    
    if not all(col in df.columns for col in required_columns):
        missing = set(required_columns) - set(df.columns)
        return {"error": f"Missing columns in CSV: {missing}"}

    df_for_prediction = df[required_columns]
    predictions = model.predict(df_for_prediction)
    probabilities = model.predict_proba(df_for_prediction)[:, 1]

    df['Prediction'] = ["✅ Approved" if p == 1 else "❌ Declined" for p in predictions]
    df['Confidence'] = [f"{prob:.2f}" for prob in probabilities]

    return {"results": df.to_dict('records')}