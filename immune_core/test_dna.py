from dna_features import encode_dna

sample_event = {
    "orig_bytes": 5000,
    "resp_bytes": 3000,
    "src_port": 34567,
    "dest_port": 22,
    "proto": "tcp"
}

dna = encode_dna(sample_event)

print("BioGuard DNA Vector:")
print(dna)
