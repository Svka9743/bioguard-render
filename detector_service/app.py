import os
from flask import Flask, request, jsonify
import torch
import joblib
import numpy as np
import requests
import os
from model.model import Autoencoder

app = Flask(__name__)

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "..", "model")

scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
model_path = os.path.join(MODEL_DIR, "autoencoder.pth")

# Load model + scaler
scaler = joblib.load(scaler_path)

model = Autoencoder(input_dim = 13)

print("Autoencoder input dim =", model.encoder[0].in_features)

model.load_state_dict(torch.load(model_path, map_location="cpu"))
model.eval()

# Environment variables
THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "1.0"))
AUTOMATION_WEBHOOK = os.getenv("AUTOMATION_WEBHOOK")

print("Automation webhook:", AUTOMATION_WEBHOOK)

def anomaly_score(features):
    x = scaler.transform([features])
    xt = torch.tensor(x, dtype=torch.float32)

    with torch.no_grad():
        out = model(xt)
        mse = torch.mean((out - xt) ** 2).item()

    return mse


@app.route("/api/detect", methods=["POST"])
def detect():
    data = request.get_json()

    feats = np.array(data["features"], dtype=float)
    meta = data.get("meta", {})

    score = anomaly_score(feats)

    anomaly = score > THRESHOLD

    response = {
        "score": score,
        "threshold": THRESHOLD,
        "anomaly": anomaly,
        "meta": meta
    }

    # CALL AUTOMATION SERVICE
    if AUTOMATION_WEBHOOK:
        try:
            r = requests.post(
                AUTOMATION_WEBHOOK,
                json=response,
                timeout=10
            )
            print("Automation response:", r.status_code, r.text)
        except Exception as e:
            print("Automation error:", e)

    return jsonify(response)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
