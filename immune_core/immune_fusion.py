"""
BioGuard Immune Fusion Engine
Combines NSA + Self-Distance detection
"""

from immune_matcher import immune_detect
from self_distance_detector import self_distance_detect


def immune_fusion_detect(event):

    nsa_detect, nsa_score = immune_detect(event)
    self_detect, self_dist = self_distance_detect(event)

    # Fusion logic
    if nsa_detect:
        return "CRITICAL", "Foreign detector match"

    if self_detect:
        return "HIGH", f"Self deviation distance={self_dist:.3f}"

    return "NORMAL", "Within immune tolerance"
