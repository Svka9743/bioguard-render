from immune_matcher import immune_detect
from self_distance_detector import self_distance_detect

attack_event = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

nsa_detect, _ = immune_detect(attack_event)
self_detect, dist = self_distance_detect(attack_event)

print("NSA Detection:", nsa_detect)
print("Self-distance Detection:", self_detect)
print("Distance:", dist)
