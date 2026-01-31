import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

MODEL_PATH = "fraud_model.pkl"

def train_model(csv_path):

    print("📂 Loading dataset...")
    df = pd.read_csv(csv_path)

    # ---- OPTIONAL BUT HIGHLY RECOMMENDED ----
    # dataset has 6.3 million rows → sample for faster training
    if len(df) > 600000:
        df = df.sample(500000, random_state=42)
        print("⚠️ Using 500,000 rows for faster training")

    print("✔ Data Loaded:", df.shape)

    features = [
        "step",
        "type",
        "amount",
        "oldbalanceOrg",
        "newbalanceOrig",     # <-- Correct Name
        "oldbalanceDest",
        "newbalanceDest"
    ]

    print("🛠 Selecting features...")
    X = df[features]
    y = df["isFraud"]

    categorical = ["type"]
    numeric = [c for c in X.columns if c not in categorical]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
            ("num", "passthrough", numeric),
        ]
    )

    print("🌲 Initializing Random Forest...")
    model = RandomForestClassifier(
        n_estimators=200,          # reduced to avoid hanging
        class_weight="balanced",
        random_state=42,
        n_jobs=-1                  # use all CPU cores
    )

    pipeline = Pipeline(steps=[
        ("preprocess", preprocessor),
        ("model", model)
    ])

    print("✂️ Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("🚀 Training model... please wait")
    pipeline.fit(X_train, y_train)

    print("\n📊 Model Evaluation Report\n")
    preds = pipeline.predict(X_test)
    print(classification_report(y_test, preds))

    joblib.dump(pipeline, MODEL_PATH)
    print("\n💾 Model saved successfully as fraud_model.pkl ✔")

def load_model():
    return joblib.load(MODEL_PATH)

if __name__ == "__main__":
    train_model("Fraud.csv")
