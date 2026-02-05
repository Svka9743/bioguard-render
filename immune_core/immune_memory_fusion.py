"""
BioGuard Adaptive Immune Fusion
"""

from immune_matcher import immune_detect
from self_distance_detector import self_distance_detect
from immune_memory import memory_detect


def adaptive_immune_detect(event):

    memory_hit, mem_dist = memory_detect(event)

    if memory_hit:
        return "CRITICAL", "Known attack — immune memory match"

    nsa_hit, _ = immune_detect(event)
    self_hit, self_dist = self_distance_detect(event)

    if nsa_hit:
        return "CRITICAL", "Foreign detector match"

    if self_hit:
        return "HIGH", f"Self deviation {self_dist:.2f}"

    return "NORMAL", "Within immune tolerance"
