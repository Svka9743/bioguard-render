import numpy as np

samples = []

for _ in range(2000):

    orig_bytes = np.random.randint(15000, 30000)
    resp_bytes = np.random.randint(10, 500)

    src_port = np.random.randint(60000, 65535)
    dest_port = 22  # SSH brute force

    samples.append([
        orig_bytes,
        resp_bytes,
        src_port,
        dest_port
    ])

np.save("anomaly_space.npy", np.array(samples))

print("Anomaly space created")
