from immune_memory import store_attack_memory

attack_event = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

store_attack_memory(attack_event)
