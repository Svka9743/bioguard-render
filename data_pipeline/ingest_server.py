from flask import Flask, request, jsonify
from feature_extractor import extract_features
import requests

# HARD-CODED detector URL (no env bug, no newline issues)
DETECTOR_URL = "https://bioguard-detector.onrender.com/api/detect"

app = Flask(__name__)


@app.route("/ingest", methods=["POST"])
def ingest():
    data = request.get_json()

    # Allow single event or list
    events = data if isinstance(data, list) else [data]

    results = []

    for e in events:
        try:
            # Extract features
            feats = extract_features(e)

            payload = {
                "features": feats.tolist(),
                "meta": {
                    "src": e.get("src_ip"),
                    "dest": e.get("dest_ip"),
                    "timestamp": e.get("timestamp")
                }
            }

            # Call detector service
            r = requests.post(
                DETECTOR_URL,
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=30
            )

            # DEBUG LOGS (visible in Render logs)
            print("Detector status:", r.status_code)
            print("Detector raw response:", r.text)

            if r.status_code == 200:
                results.append(r.json())
            else:
                results.append({
                    "error": "Detector error",
                    "status": r.status_code,
                    "raw": r.text
                })

        except Exception as ex:
            results.append({"error": str(ex)})

    return jsonify(results)


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
