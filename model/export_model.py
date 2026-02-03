import sys
import os
import torch

# Absolute path to project root
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add model folder directly to Python path
MODEL_DIR = os.path.join(PROJECT_ROOT, "model")
sys.path.append(MODEL_DIR)

from model import Autoencoder   # this imports model.py inside model folder

# Load trained model (13 features)
model = Autoencoder(13)
model.load_state_dict(torch.load(os.path.join(MODEL_DIR, "autoencoder.pth"), map_location="cpu"))
model.eval()

# Convert to TorchScript
scripted = torch.jit.script(model)

# Save TorchScript model
scripted.save(os.path.join(MODEL_DIR, "model_ts.pt"))

print("TorchScript model saved successfully")
