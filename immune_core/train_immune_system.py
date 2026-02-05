import numpy as np
from dna_features import encode_dna
from negative_selection import train_detectors

normal_data = np.load("baseline_realistic.npy")
anomaly_data = np.load("anomaly_space.npy")

#  Combine normal + anomaly
combined = np.vstack([normal_data, anomaly_data])

dna_dataset = []

#  Convert COMBINED data instead of raw_data # Combine normal + anomaly

for row in combined:

    event = {
        "orig_bytes": row[0],
        "resp_bytes": row[1],
        "src_port": row[2],
        "dest_port": row[3],
        "proto": "tcp"
    }

    dna = encode_dna(event)
    dna_dataset.append(dna)

dna_dataset = np.array(dna_dataset)

print("Training detectors...")

detectors = train_detectors(dna_dataset)

centers = [d.center for d in detectors]

# Debug print
print("Sample detector center:", centers[0])

np.save("immune_detectors.npy", np.array(centers))

print("Detectors created:", len(centers))
