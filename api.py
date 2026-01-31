from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from model import load_model

app = FastAPI(title="Aegis Fraud Detection API")

model = load_model()

class Transaction(BaseModel):
    step: int
    type: str
    amount: float
    oldbalanceOrg: float
    newbalanceOrig: float
    oldbalanceDest: float
    newbalanceDest: float

@app.get("/")
def home():
    return {"message": "Aegis Fraud Detection API Running"}

@app.post("/predict")
def predict(tx: Transaction):
    data = pd.DataFrame([{
        "step": tx.step,
        "type": tx.type,
        "amount": tx.amount,
        "oldbalanceOrg": tx.oldbalanceOrg,
        "newbalanceOrig": tx.newbalanceOrig,
        "oldbalanceDest": tx.oldbalanceDest,
        "newbalanceDest": tx.newbalanceDest
    }])

    prob = model.predict_proba(data)[0][1]
    is_fraud = prob > 0.7

    return {
        "fraud_probability": round(float(prob), 4),
        "is_fraud": bool(is_fraud)
    }
