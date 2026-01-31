# 🔐 Project Aegis – Real-time Transaction Fraud Detection System

**Aegis** is an end-to-end real-time fraud detection system that simulates live financial transactions, detects fraudulent behavior using a machine learning model, and visualizes results through an interactive dashboard.

This project demonstrates how traditional batch-based fraud detection can be transformed into a **real-time streaming architecture** using modern Python tools.

---

## 🚀 Key Features

- 📊 Machine Learning Fraud Detection Model trained on PaySim dataset  
- ⚡ Real-time Fraud Scoring API using FastAPI  
- 🔁 Live Transaction Stream Simulation  
- 📈 Interactive Live Dashboard using Streamlit  
- 🛑 Instant Fraud Detection & Blocking  

---

## 🧠 Use Case

A customer makes a local transaction followed by a high-value transfer.  
Aegis processes the transaction in real-time, assigns a fraud probability, blocks suspicious activity instantly, and prevents financial loss.

---

## 🗂 Project Structure

Aegis-Fraud-Detection/
│
├── model.py # Train and save ML model
├── api.py # FastAPI inference service
├── producer.py # Live transaction simulator
├── dashboard.py # Streamlit fraud monitoring dashboard
├── fraud_model.pkl # Trained model file
├── Fraud.csv # PaySim dataset
├── requirements.txt
└── README.md


---

## 📊 Dataset Information

Dataset: **PaySim – Simulated Financial Transactions**

- Rows: 6,362,620  
- Columns: 10  

### Data Dictionary

| Column | Description |
|------|------------|
| step | Time unit (1 step = 1 hour, total 744 steps) |
| type | CASH_IN, CASH_OUT, DEBIT, PAYMENT, TRANSFER |
| amount | Transaction amount |
| nameOrig | Sender account |
| oldbalanceOrg | Sender balance before transaction |
| newbalanceOrig | Sender balance after transaction |
| nameDest | Receiver account |
| oldbalanceDest | Receiver balance before transaction |
| newbalanceDest | Receiver balance after transaction |
| isFraud | Fraud label (1 = Fraud) |
| isFlaggedFraud | Rule-based flagged fraud |

---

## 🧪 Machine Learning Model

- Algorithm: **Random Forest Classifier**
- Handles class imbalance using `class_weight="balanced"`
- Preprocessing:
  - One-Hot Encoding for transaction type
  - Numerical features passthrough
- Output:
  - Fraud Probability
  - Fraud / Not Fraud classification

---

## 🛠 Tech Stack

- Python
- Pandas
- Scikit-learn
- FastAPI
- Uvicorn
- Streamlit
- Joblib

---

## ⚙️ Setup Instructions

### 1️⃣ Create Virtual Environment (Recommended)

python -m venv venv

Activate the virtual environment:

**Windows**
venv\Scripts\activate

**Linux / macOS**
source venv/bin/activate

### 2️⃣ Install Dependencies

pip install -r requirements.txt

---

## 🏗 Train the Model

Ensure `Fraud.csv` is present in the project directory.

python model.py

This will:
- Train the fraud detection model
- Print evaluation metrics
- Save `fraud_model.pkl`

---

## 🚀 Run the FastAPI Server

uvicorn api:app --reload

API URL:
http://127.0.0.1:8000

Swagger UI:
http://127.0.0.1:8000/docs

---

## 🔁 Run Transaction Producer

Simulates live transactions and sends them to the API.

python producer.py

---

## 📈 Run Live Dashboard

streamlit run dashboard.py

Dashboard URL:
http://localhost:8501

---

## 📊 Dashboard Features

- Total transactions processed
- Fraud detected count
- Fraud rate percentage
- Live scatter plot (Amount vs Time)
- Real-time transaction logs

## ✅ Project Outcome

- End-to-end real-time fraud detection pipeline
- Live monitoring dashboard
- Production-style ML inference API