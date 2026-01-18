import numpy as np
import joblib
import torch
from model import Autoencoder


# Load training data
X = np.load("model/normal_data.npy")

# Load scaler and model
scaler = joblib.load("model/scaler.pkl")
model = Autoencoder(input_dim=12)
model.load_state_dict(torch.load("model/autoencoder.pth", map_location="cpu"))
model.eval()

errors = []

# Compute reconstruction error for each normal sample
for row in X:
    x = scaler.transform([row])
    xt = torch.tensor(x, dtype=torch.float32)
    with torch.no_grad():
        out = model(xt)
        mse = torch.mean((out - xt) ** 2).item()
    errors.append(mse)

# Calculate 99th percentile threshold
threshold = np.percentile(errors, 99)

print("===================================")
print("BioGuard Recommended Threshold")
print("99th Percentile Value:", threshold)
print("===================================")
