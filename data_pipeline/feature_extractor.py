import datetime
import ipaddress
import numpy as np

# ---------------------------
# FLOW AGGREGATION CACHE
# ---------------------------
flow_cache = {}

def aggregate(ip, size):
    if ip not in flow_cache:
        flow_cache[ip] = 0
    flow_cache[ip] += size
    return flow_cache[ip]

# ---------------------------
# TIME BUCKET (3 FEATURES)
# ---------------------------
def time_of_day_bucket(ts):
    if isinstance(ts, str):
        dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
    else:
        dt = datetime.datetime.utcfromtimestamp(ts / 1000)

    h = dt.hour

    # Night (00–06), Day (06–18), Evening (18–24)
    if 0 <= h < 6:
        return [1, 0, 0]
    elif 6 <= h < 18:
        return [0, 1, 0]
    else:
        return [0, 0, 1]

# ---------------------------
# FEATURE EXTRACTOR
# ---------------------------
def extract_features(eve_json):
    src = eve_json.get("src_ip", "")
    proto = eve_json.get("proto", "tcp")

    src_port = int(eve_json.get("src_port", 0) or 0)
    dest_port = int(eve_json.get("dest_port", 0) or 0)

    size = int(eve_json.get("orig_bytes", 0) or 0) + int(eve_json.get("resp_bytes", 0) or 0)

    pkts = int(eve_json.get("pkts", 0) or 0)

    ts = eve_json.get("timestamp", None)

    tod = time_of_day_bucket(ts) if ts else [0, 0, 0]

    proto_enc = [1, 0, 0] if proto == "tcp" else ([0, 1, 0] if proto == "udp" else [0, 0, 1])

    well_known = 1 if dest_port in (22, 80, 443, 3389, 21) else 0

    src_is_private = 1 if src and ipaddress.ip_address(src).is_private else 0

    # ---------------------------
    # FLOW WINDOW FEATURE
    # ---------------------------
    flow_bytes = aggregate(src, size)

    # ---------------------------
    # FINAL FEATURE VECTOR
    # ---------------------------
    feats = (
        [size, pkts, src_port, dest_port, well_known, src_is_private]
        + proto_enc
        + tod
        + [flow_bytes]

    )

    while len(feats) < 13:
        feats.append(0)

    return np.array(feats, dtype=float)
