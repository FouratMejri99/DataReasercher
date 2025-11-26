import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report
import joblib
import json

MODEL_DIR = "outputs/models"
os.makedirs(MODEL_DIR, exist_ok=True)

def _prepare(df, target):
    # simple preprocessing: drop non-numeric except we label-encode categoricals
    X = df.drop(columns=[target])
    y = df[target]
    encoders = {}
    for col in X.select_dtypes(include="object").columns:
        le = LabelEncoder()
        X[col] = X[col].fillna("nan").astype(str)
        X[col] = le.fit_transform(X[col])
        encoders[col] = le
    # target encode if necessary
    if y.dtype == object or y.dtype.name == "category":
        tenc = LabelEncoder()
        y = tenc.fit_transform(y.astype(str))
    else:
        tenc = None
    return X.fillna(0), y, encoders, tenc

def train_models(csv_path, target_column, test_size=0.2, random_state=42):
    df = pd.read_csv(csv_path)
    if target_column not in df.columns:
        raise ValueError("Target column not in CSV")
    X, y, encoders, tenc = _prepare(df, target_column)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Logistic Regression
    lr = LogisticRegression(max_iter=1000)
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    acc_lr = accuracy_score(y_test, y_pred_lr)

    # Random Forest
    rf = RandomForestClassifier(n_estimators=100, random_state=random_state)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    acc_rf = accuracy_score(y_test, y_pred_rf)

    # Save models + encoders
    base = os.path.basename(csv_path).replace(".csv","")
    lr_path = f"{MODEL_DIR}/{base}_lr.joblib"
    rf_path = f"{MODEL_DIR}/{base}_rf.joblib"
    enc_path = f"{MODEL_DIR}/{base}_encoders.joblib"
    tenc_path = f"{MODEL_DIR}/{base}_tenc.joblib"

    joblib.dump(lr, lr_path)
    joblib.dump(rf, rf_path)
    joblib.dump(encoders, enc_path)
    joblib.dump(tenc, tenc_path)

    result = {
        "lr_accuracy": float(acc_lr),
        "rf_accuracy": float(acc_rf),
        "lr_model": lr_path,
        "rf_model": rf_path,
        "encoders": enc_path,
        "tenc": tenc_path
    }
    # also save a report
    with open(f"outputs/{base}_ml_report.json", "w") as f:
        json.dump(result, f)
    return result

def predict(csv_path, input_row: dict, model_type="rf"):
    # load model and encoders for csv_path base name
    base = os.path.basename(csv_path).replace(".csv","")
    model_path = f"{MODEL_DIR}/{base}_{'rf' if model_type=='rf' else 'lr'}.joblib"
    enc_path = f"{MODEL_DIR}/{base}_encoders.joblib"
    tenc_path = f"{MODEL_DIR}/{base}_tenc.joblib"
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model not trained — run train_models first")

    model = joblib.load(model_path)
    encoders = joblib.load(enc_path)
    tenc = joblib.load(tenc_path)

    # create DataFrame of one row
    df = pd.DataFrame([input_row])
    for col, le in (encoders or {}).items():
        if col in df:
            df[col] = df[col].astype(str)
            df[col] = le.transform(df[col])
    X = df.fillna(0)
    pred = model.predict(X)[0]
    # inverse transform if tenc present
    if tenc is not None:
        try:
            pred = tenc.inverse_transform([int(pred)])[0]
        except Exception:
            pass
    return {"prediction": pred}
