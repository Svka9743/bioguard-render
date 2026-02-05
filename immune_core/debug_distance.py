import numpy as np
from dna_features import encode_dna

detectors = np.load("immune_detectors.npy")

attack_event = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

dna = encode_dna(attack_event)

distances = []

for detector in detectors:
    dist = np.linalg.norm(detector - dna)
    distances.append(dist)

print("Min distance to attack:", min(distances))
print("Max distance:", max(distances))
