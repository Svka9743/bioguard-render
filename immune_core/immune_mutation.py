"""
Detects attack mutations + lineage similarity
"""

import numpy as np
from dna_features import encode_dna
from immune_threat_db import threat_db


def detect_mutation(event):

    if len(threat_db) == 0:
        return False, None

    dna = encode_dna(event)

    distances = []

    for threat in threat_db:
        dist = np.linalg.norm(dna - threat["dna"])
        distances.append(dist)

    min_dist = min(distances)

    if min_dist < 0.50:
        return True, min_dist

    return False, min_dist
