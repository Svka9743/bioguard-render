"""
BioGuard Threat Evolution Engine
"""

from immune_memory_fusion import adaptive_immune_detect
from immune_mutation import detect_mutation
from immune_threat_db import store_threat
from immune_detector_evolution import evolve_detectors


def evolve_threat_response(event):

    level, reason = adaptive_immune_detect(event)

    mutation_hit, mutation_dist = detect_mutation(event)

    # Evolution logic
    if mutation_hit:
        level = "CRITICAL"
        reason = f"Attack mutation detected dist={mutation_dist:.2f}"
    
    # Evolve detectors if threat high
    if level in ["HIGH", "CRITICAL"]:
        evolve_detectors(event)


    # Store threat in DB
    store_threat(event, level)

    return level, reason
