from immune_matcher import immune_detect
from dna_features import encode_dna

attack_event = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

dna = encode_dna(attack_event)

print("Attack DNA Vector:")
print(dna)

detected, score = immune_detect(attack_event)

print("Immune Detection:", detected)
print("Match Score:", score)
