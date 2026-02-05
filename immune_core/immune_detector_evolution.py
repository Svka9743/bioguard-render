"""
BioGuard Detector Evolution Engine
Mutates detectors toward attack DNA
"""

import numpy as np
from dna_features import encode_dna

DETECTOR_FILE = "immune_detectors.npy"


def evolve_detectors(event):

    detectors = np.load(DETECTOR_FILE)

    # Backup detectors BEFORE evolution
    np.save("immune_detectors_backup.npy", detectors)

    attack_dna = encode_dna(event)

    evolved_detectors = []

    for detector in detectors:

        # Move detector slightly toward attack DNA
        distance = np.linalg.norm(attack_dna - detector)

        mutation_strength = min(0.80, distance)

        mutation_vector = (attack_dna - detector) * mutation_strength

        new_detector = detector + mutation_vector

        evolved_detectors.append(new_detector)

    np.save(DETECTOR_FILE, np.array(evolved_detectors))

    print("Detectors evolved toward threat space")
