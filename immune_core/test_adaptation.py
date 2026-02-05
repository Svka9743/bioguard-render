from immune_evolution_engine import evolve_threat_response
from immune_matcher import immune_detect

attack_event = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

print("Before evolution:")
print(immune_detect(attack_event))

# Trigger evolution
evolve_threat_response(attack_event)

print("\nAfter evolution:")
print(immune_detect(attack_event))
