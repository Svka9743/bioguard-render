from immune_evolution_engine import evolve_threat_response

# Original attack
attack1 = {
    "orig_bytes": 20000,
    "resp_bytes": 10,
    "src_port": 65000,
    "dest_port": 22,
    "proto": "tcp"
}

# Mutated attack
attack2 = {
    "orig_bytes": 21000,
    "resp_bytes": 15,
    "src_port": 64000,
    "dest_port": 22,
    "proto": "tcp"
}

print("First attack:")
print(evolve_threat_response(attack1))

print("\nMutated attack:")
print(evolve_threat_response(attack2))
