import numpy as np

# Load detectors BEFORE evolution
before = np.load("immune_detectors_backup.npy")

# Load detectors AFTER evolution
after = np.load("immune_detectors.npy")

# Calculate total shift
diff = np.linalg.norm(after - before)


print("Total detector shift:", diff)
