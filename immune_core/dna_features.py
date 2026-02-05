import numpy as np

def encode_dna(event):

    packet_size = int(event.get("orig_bytes", 0))
    response_size = int(event.get("resp_bytes", 0))

    src_port = int(event.get("src_port", 0))
    dest_port = int(event.get("dest_port", 0))

    protocol = event.get("proto", "tcp")

    # Protocol genes
    proto_tcp = 1 if protocol == "tcp" else 0
    proto_udp = 1 if protocol == "udp" else 0
    proto_other = 1 if protocol not in ["tcp", "udp"] else 0

    # Normalize traffic size
    packet_size_norm = min(packet_size / 10000, 1.0)
    response_size_norm = min(response_size / 10000, 1.0)

    # Normalize ports
    src_port_norm = src_port / 65535
    dest_port_norm = dest_port / 65535

    # NEW BEHAVIORAL GENES

    brute_force_gene = 1 if dest_port == 22 else 0
    data_exfil_gene = 1 if packet_size > 8000 else 0
    api_abuse_gene = 1 if dest_port in [80, 443] and packet_size > 5000 else 0

    dna_vector = [
        packet_size_norm,
        response_size_norm,
        src_port_norm,
        dest_port_norm,
        proto_tcp,
        proto_udp,
        proto_other,
        brute_force_gene,
        data_exfil_gene,
        api_abuse_gene
    ]

    return np.array(dna_vector)
