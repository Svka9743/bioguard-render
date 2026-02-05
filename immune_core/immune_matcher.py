import numpy as np
from dna_features import encode_dna

DETECTOR_RADIUS = 0.80

detectors = np.load("immune_detectors.npy")


def immune_detect(event):

    dna = encode_dna(event)

    for detector in detectors:

        dist = np.linalg.norm(detector - dna)

        if dist < DETECTOR_RADIUS:
            return True, dist

    return False, None
