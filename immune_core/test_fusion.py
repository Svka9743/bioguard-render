from immune_fusion import immune_fusion_detect

attack_event = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

level, reason = immune_fusion_detect(attack_event)

print("Threat Level:", level)
print("Reason:", reason)
