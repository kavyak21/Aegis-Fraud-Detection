import time
import random
import requests

API_URL = "http://127.0.0.1:8000/predict"

transaction_types = ["PAYMENT", "CASH_OUT", "TRANSFER", "DEBIT", "CASH_IN"]

def generate_transaction():
    return {
        "step": random.randint(1, 744),
        "type": random.choice(transaction_types),
        "amount": round(random.uniform(10, 500000), 2),
        "oldbalanceOrg": round(random.uniform(0, 600000), 2),
        "newbalanceOrig": 0.0,
        "oldbalanceDest": round(random.uniform(0, 600000), 2),
        "newbalanceDest": 0.0
    }

while True:
    tx = generate_transaction()
    tx["newbalanceOrig"] = max(tx["oldbalanceOrg"] - tx["amount"], 0)
    tx["newbalanceDest"] = tx["oldbalanceDest"] + tx["amount"]

    response = requests.post(API_URL, json=tx)
    
    print("Transaction:", tx)
    print("Response:", response.json())
    print("-" * 50)

    time.sleep(2)
