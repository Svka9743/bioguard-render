"""
BioGuard Immune Memory Bank
Stores and recalls attack DNA
"""

import numpy as np
import os
from dna_features import encode_dna

MEMORY_FILE = "immune_memory.npy"


# Load memory if exists
if os.path.exists(MEMORY_FILE):
    immune_memory = list(np.load(MEMORY_FILE))
else:
    immune_memory = []


def store_attack_memory(event):

    dna = encode_dna(event)

    immune_memory.append(dna)

    np.save(MEMORY_FILE, np.array(immune_memory))

    print("Attack DNA stored in immune memory")


def memory_detect(event):

    if len(immune_memory) == 0:
        return False, None

    dna = encode_dna(event)

    distances = []

    for mem in immune_memory:
        dist = np.linalg.norm(dna - mem)
        distances.append(dist)

    min_dist = min(distances)

    if min_dist < 0.80:
        return True, min_dist

    return False, min_dist
