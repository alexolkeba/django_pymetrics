import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
import os

# ---- 1. Synthetic Data Generation ----

NUM_CANDIDATES = 2000
NUM_GAMES = 12
GAME_FEATURES = ['score', 'mean_reaction_time', 'accuracy']
NUM_TRAITS = 8

def generate_synthetic_data(n=NUM_CANDIDATES):
    X = []
    y_traits = []
    y_recommend = []
    for _ in range(n):
        candidate_features = []
        for _ in range(NUM_GAMES):
            score = np.random.uniform(0, 100)
            rt = np.random.uniform(200, 1200)  # ms
            acc = np.random.uniform(0.5, 1.0)
            candidate_features.extend([score, rt, acc])
        # Traits: random floats, but correlated with some features
        traits = np.tanh(np.array(candidate_features[:NUM_TRAITS]) / 100)
        traits += np.random.normal(0, 0.1, size=NUM_TRAITS)
        traits = np.clip(traits, 0, 1)
        # Recommendation: simple rule for demo
        rec = int(traits.mean() > 0.7) + int(traits.mean() > 0.85)
        X.append(candidate_features)
        y_traits.append(traits)
        y_recommend.append(rec)
    return np.array(X, dtype=np.float32), np.array(y_traits, dtype=np.float32), np.array(y_recommend, dtype=np.int64)

X, y_traits, y_recommend = generate_synthetic_data()

# ---- 2. PyTorch Model ----

class TraitNet(nn.Module):
    def __init__(self, input_dim, num_traits, num_classes):
        super().__init__()
        self.shared = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
        )
        self.trait_head = nn.Linear(32, num_traits)
        self.rec_head = nn.Linear(32, num_classes)
    def forward(self, x):
        h = self.shared(x)
        traits = torch.sigmoid(self.trait_head(h))
        rec = self.rec_head(h)
        return traits, rec

input_dim = NUM_GAMES * len(GAME_FEATURES)
model = TraitNet(input_dim, NUM_TRAITS, 3)

# ---- 3. Training ----

BATCH_SIZE = 64
EPOCHS = 30
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
loss_traits = nn.MSELoss()
loss_rec = nn.CrossEntropyLoss()

dataset = TensorDataset(torch.tensor(X), torch.tensor(y_traits), torch.tensor(y_recommend))
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)

for epoch in range(EPOCHS):
    model.train()
    total_loss = 0
    for xb, yb_traits, yb_rec in loader:
        optimizer.zero_grad()
        pred_traits, pred_rec = model(xb)
        loss = loss_traits(pred_traits, yb_traits) + loss_rec(pred_rec, yb_rec)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    if (epoch+1) % 5 == 0:
        print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {total_loss/len(loader):.4f}")

# ---- 4. Export Model ----

os.makedirs("ai_model", exist_ok=True)
torch.save(model.state_dict(), "ai_model/model.pth")
print("Model saved to ai_model/model.pth") 