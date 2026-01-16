from flask import Flask, request, jsonify
from feature_extractor import extract_features
import requests
import os

DETECTOR_URL = os.getenv("DETECTOR_URL", "http://detector:5000/api/detect")

app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()
    events = data if isinstance(data, list) else [data]
    results = []

    for e in events:
        try:
            feats = extract_features(e)
            payload = {
                "features": feats.tolist(),
                "meta": {
                    "src": e.get("src_ip"),
                    "dest": e.get("dest_ip"),
                    "timestamp": e.get("timestamp")
                }
            }
            r = requests.post(DETECTOR_URL, json=payload, timeout=20)
            results.append(r.json())

        except Exception as ex:
            results.append({"error": str(ex)})

    return jsonify(results)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
