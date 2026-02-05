import numpy as np

samples = []

for _ in range(5000):

    orig_bytes = np.random.randint(100, 2000)
    resp_bytes = np.random.randint(100, 2000)

    src_port = np.random.randint(1024, 65535)
    dest_port = np.random.choice([22, 21, 25, 53, 80, 110, 143, 443, 3306])


    samples.append([
        orig_bytes,
        resp_bytes,
        src_port,
        dest_port
    ])

np.save("baseline_realistic.npy", np.array(samples))

print("Baseline created")
