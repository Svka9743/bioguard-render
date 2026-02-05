from immune_memory import store_attack_memory, memory_detect

attack_event = {
    "orig_bytes": 21000,
    "resp_bytes": 15,
    "src_port": 64000,
    "dest_port": 22,
    "proto": "tcp"
}

# Store attack DNA
store_attack_memory(attack_event)

# Test recall
detected, dist = memory_detect(attack_event)

print("Memory Detection:", detected)
print("Memory Distance:", dist)
