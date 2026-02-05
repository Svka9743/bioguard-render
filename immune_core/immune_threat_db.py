"""
BioGuard Threat Evolution Database
Tracks attack families + mutations
"""

import numpy as np
import os
from dna_features import encode_dna

THREAT_DB_FILE = "immune_threat_db.npy"

if os.path.exists(THREAT_DB_FILE):
    threat_db = list(np.load(THREAT_DB_FILE, allow_pickle=True))
else:
    threat_db = []


def store_threat(event, severity):

    dna = encode_dna(event)

    threat_db.append({
        "dna": dna,
        "severity": severity
    })

    np.save(THREAT_DB_FILE, threat_db)

    print("Threat stored in evolution database")
