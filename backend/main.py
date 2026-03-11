from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from typing import List

app = FastAPI()

# Load models into memory at startup, NOT inside the endpoint
try:
    model = joblib.load('sleep_model.pkl')
    # scaler = joblib.load('scaler.pkl') # Uncomment if using a scaler
except Exception as e:
    raise RuntimeError(f"Failed to load model artifacts: {e}")

# Define the exact strict schema expected from the frontend
class SleepDataInput(BaseModel):
    heart_rate: List[float]
    # respiration: List[float] # Add other features your model needs

@app.post("/predict")
async def predict_stages(data: SleepDataInput):
    try:
        # 1. Convert input to DataFrame or Numpy array
        input_data = np.array(data.heart_rate).reshape(-1, 1)
        
        # 2. Preprocess (if applicable)
        # input_data = scaler.transform(input_data)
        
        # 3. Predict
        predictions = model.predict(input_data)
        
        # 4. Return as a native Python list so FastAPI can serialize to JSON
        return {"stages": predictions.tolist()}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))