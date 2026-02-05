"""
BioGuard Negative Selection with Hypersphere Detectors
"""

import numpy as np

NUM_DETECTORS = 2000
SELF_RADIUS = 0.15
DETECTOR_RADIUS = 0.80


class Detector:

    def __init__(self, center):
        self.center = center
        self.radius = DETECTOR_RADIUS


def distance(a, b):
    return np.linalg.norm(a - b)


def generate_random_detector(dna_length=10):
    # Focus detectors near self boundary
    center = np.random.uniform(0.2, 1.0, dna_length)
    return Detector(center)


def overlaps_self(detector, self_dna):

    for dna in self_dna:

        if distance(detector.center, dna) < SELF_RADIUS:
            return True

    return False


def train_detectors(self_dataset):

    detectors = []

    while len(detectors) < NUM_DETECTORS:

        candidate = generate_random_detector()

        if not overlaps_self(candidate, self_dataset):
            detectors.append(candidate)

    return detectors
