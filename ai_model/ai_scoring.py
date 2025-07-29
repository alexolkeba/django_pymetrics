import torch
import torch.nn as nn
import numpy as np
import os

NUM_GAMES = 12
GAME_FEATURES = ['score', 'mean_reaction_time', 'accuracy']
NUM_TRAITS = 8

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

def load_model():
    input_dim = NUM_GAMES * len(GAME_FEATURES)
    model = TraitNet(input_dim, NUM_TRAITS, 3)
    model_path = os.path.join(os.path.dirname(__file__), "model.pth")
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model

def predict_traits_and_recommendation(game_data):
    """
    game_data: list of floats, length = NUM_GAMES * len(GAME_FEATURES)
    """
    model = load_model()
    x = torch.tensor([game_data], dtype=torch.float32)
    with torch.no_grad():
        traits, rec = model(x)
    traits = traits.numpy().flatten().tolist()
    rec = int(torch.argmax(rec, dim=1).item())
    return traits, rec 