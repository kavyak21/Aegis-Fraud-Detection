import streamlit as st
import requests
import random
import pandas as pd
from datetime import datetime

API_URL = "http://127.0.0.1:8000/predict"

st.set_page_config(page_title="Aegis: Live Fraud Monitor", layout="wide")

st.title("🛡️ Aegis: Live Fraud Monitor (Advanced)")

transaction_types = ["PAYMENT", "CASH_OUT", "TRANSFER", "DEBIT", "CASH_IN"]

# Maintain session history
if "logs" not in st.session_state:
    st.session_state.logs = []

# Generate Random Transaction
def generate_transaction():
    tx = {
        "step": random.randint(1, 744),
        "type": random.choice(transaction_types),
        "amount": round(random.uniform(50, 20000), 2),
        "oldbalanceOrg": round(random.uniform(0, 40000), 2),
        "newbalanceOrig": 0.0,
        "oldbalanceDest": round(random.uniform(0, 40000), 2),
        "newbalanceDest": 0.0
    }

    tx["newbalanceOrig"] = max(tx["oldbalanceOrg"] - tx["amount"], 0)
    tx["newbalanceDest"] = tx["oldbalanceDest"] + tx["amount"]

    return tx


# ---- LIVE SIMULATION BUTTON ----
colA, colB = st.columns([1,4])
with colA:
    if st.button("▶️ Start Simulation"):
        st.session_state.running = True
    if st.button("⏹ Stop Simulation"):
        st.session_state.running = False

if "running" not in st.session_state:
    st.session_state.running = False


# ---- METRICS SECTION ----
col1, col2, col3 = st.columns(3)

total_tx = len(st.session_state.logs)
fraud_tx = sum(1 for x in st.session_state.logs if x["is_fraud"] == True)
fraud_rate = (fraud_tx / total_tx * 100) if total_tx > 0 else 0

col1.metric("Recent Transactions", total_tx)
col2.metric("Fraud Detected", fraud_tx)
col3.metric("Fraud Rate", f"{fraud_rate:.1f}%")

st.markdown("---")

# ---- LIVE DATA GENERATION ----
if st.session_state.running:
    tx = generate_transaction()
    try:
        res = requests.post(API_URL, json=tx)
        result = res.json()

        st.session_state.logs.append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "amount": tx["amount"],
            "step": tx["step"],
            "type": tx["type"],
            "fraud_probability": result.get("fraud_probability", 0),
            "is_fraud": result.get("is_fraud", False)
        })

    except Exception as e:
        st.error(f"API Error: {e}")


# Convert to DataFrame
if len(st.session_state.logs) > 0:
    df = pd.DataFrame(st.session_state.logs)

    left, right = st.columns(2)

    # ---- SCATTER PLOT ----
    with left:
        st.subheader("📊 Transaction Analysis")
        df_plot = df.copy()
        df_plot["status"] = df_plot["is_fraud"].apply(lambda x: "BLOCKED" if x else "APPROVED")

        st.scatter_chart(
            df_plot,
            x="timestamp",
            y="amount",
            color="status"
        )

    # ---- LIVE LOG TABLE ----
    with right:
        st.subheader("📝 Recent Logs (Live)")
        st.dataframe(df[::-1], height=400)

else:
    st.info("Click ▶️ Start Simulation to begin live monitoring.")
    

st.markdown("---")
st.caption("Powered by FastAPI + Streamlit | Aegis Fraud Detection System")
