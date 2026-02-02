import json
import numpy as np
import sys
import os

# Add project root to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from data_pipeline.feature_extractor import extract_features

features = []

with open("eve.json") as f:
    for line in f:
        try:
            data = json.loads(line)

            # Ignore Suricata stats logs
            if data.get("event_type") == "stats":
                continue

            feat = extract_features(data)
            features.append(feat)

        except Exception as e:
            continue

X = np.array(features)

np.save("model/normal_data.npy", X)

print("Dataset created:", X.shape)
