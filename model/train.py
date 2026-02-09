import numpy as np, joblib, torch
from sklearn.preprocessing import StandardScaler
from torch.utils.data import TensorDataset, DataLoader
from model import Autoencoder

# create synthetic normal data (10000 samples, feature dim = 13)
X = np.random.normal(loc=0.0, scale=1.0, size=(10000, 13))
np.save("normal_data.npy", X)

scaler = StandardScaler()
Xs = scaler.fit_transform(X)
joblib.dump(scaler, "scaler.pkl")

Xtensor = torch.tensor(Xs, dtype=torch.float32)
dataset = TensorDataset(Xtensor, Xtensor)
loader = DataLoader(dataset, batch_size=128, shuffle=True)

model = Autoencoder(input_dim = 13)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
loss_fn = torch.nn.MSELoss()

for epoch in range(1, 11):
    epoch_loss = 0.0
    for b_x, _ in loader:
        out = model(b_x)
        loss = loss_fn(out, b_x)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        epoch_loss += loss.item()
    print(f"Epoch {epoch} loss {epoch_loss/len(loader):.6f}")

torch.save(model.state_dict(), "autoencoder.pth")
print("Saved autoencoder.pth and scaler.pkl and normal_data.npy")
