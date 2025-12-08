import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
import os, joblib, torch
from model.model import Autoencoder

app = Flask(__name__)
THRESHOLD = float(os.getenv("ANOMALY_THRESHOLD", "0.02"))

# load scaler & model (assumes files are in repo/model/)
scaler = joblib.load("model/scaler.pkl")
model = Autoencoder(input_dim=12)
model.load_state_dict(torch.load("model/autoencoder.pth", map_location="cpu"))
model.eval()

def anomaly_score(features):
    x = scaler.transform([features])
    x_t = torch.tensor(x, dtype=torch.float32)
    with torch.no_grad():
        out = model(x_t)
        mse = torch.mean((out - x_t) ** 2).item()
    return mse

@app.route("/api/detect", methods=["POST"])
def detect():
    data = request.get_json()
    feats = data.get("features")
    meta = data.get("meta", {})
    score = anomaly_score(feats)
    out = {"score": score, "threshold": THRESHOLD, "meta": meta}
    if score > THRESHOLD:
        out["anomaly"] = True
        webhook = os.getenv("AUTOMATION_WEBHOOK")
        if webhook:
            try:
                import requests
                requests.post(webhook, json={"source": meta, "score": score}, timeout=3)
            except Exception as e:
                app.logger.error("Failed to call automation: %s", e)
    else:
        out["anomaly"] = False
    return jsonify(out)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
