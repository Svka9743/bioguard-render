import numpy as np
from dna_features import encode_dna

# Load baseline DNA
baseline = np.load("baseline_realistic.npy")

# Convert to DNA
from dna_features import encode_dna

dna_baseline = []

for row in baseline:

    event = {
        "orig_bytes": row[0],
        "resp_bytes": row[1],
        "src_port": row[2],
        "dest_port": row[3],
        "proto": "tcp"
    }

    dna = encode_dna(event)
    dna_baseline.append(dna)

dna_baseline = np.array(dna_baseline)


def self_distance_detect(event):

    dna = encode_dna(event)

    distances = []

    for self_dna in dna_baseline:
        dist = np.linalg.norm(dna - self_dna)
        distances.append(dist)

    min_dist = min(distances)

    # Threshold learned empirically
    if min_dist > 0.6:
        return True, min_dist

    return False, min_dist
