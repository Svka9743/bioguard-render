import datetime, ipaddress, numpy as np

def time_of_day_bucket(ts):
    if isinstance(ts, str):
        dt = datetime.datetime.fromisoformat(ts.replace("Z","+00:00"))
    else:
        dt = datetime.datetime.utcfromtimestamp(ts/1000)
    h = dt.hour
    if 0 <= h < 6: return [1,0,0,0]
    if 6 <= h < 12: return [0,1,0,0]
    if 12 <= h < 18: return [0,0,1,0]
    return [0,0,0,1]

def extract_features(eve_json):
    src = eve_json.get("src_ip","")
    proto = eve_json.get("proto","tcp")
    src_port = int(eve_json.get("src_port",0) or 0)
    dest_port = int(eve_json.get("dest_port",0) or 0)
    size = int(eve_json.get("orig_bytes",0) or 0) + int(eve_json.get("resp_bytes",0) or 0)
    pkts = int(eve_json.get("pkts",0) or 0)
    ts = eve_json.get("timestamp", None)
    tod = time_of_day_bucket(ts) if ts else [0,0,0,0]
    proto_enc = [1,0,0] if proto=="tcp" else ([0,1,0] if proto=="udp" else [0,0,1])
    well_known = 1 if dest_port in (22,80,443,3389,21) else 0
    src_is_private = 1 if src and ipaddress.ip_address(src).is_private else 0
    feats = [size, pkts, src_port, dest_port, well_known, src_is_private] + proto_enc + tod
    return np.array(feats, dtype=float)
