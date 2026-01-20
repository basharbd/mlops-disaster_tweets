import torch
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from transformers import AutoTokenizer
from pathlib import Path

# --- FIXED IMPORT ---
# This is the standard way to import within a package.
# It requires src/disaster_tweets/__init__.py to exist.
from disaster_tweets.model import DisasterTweetModel

app = FastAPI()

# --- PATHS (Robust for both Docker and Local) ---
# We check if we are in Docker (/app exists) or Local
if os.path.exists("/app"):
    project_root = Path("/app")
else:
    # Fallback for local testing: Go up 3 levels from this file
    # src/disaster_tweets/api.py -> src/disaster_tweets -> src -> ROOT
    project_root = Path(__file__).parent.parent.parent

static_path = project_root / "static"
model_file = project_root / "models" / "best_model.ckpt"

# 1. LOAD MODEL
print(f"--- Loading Model from {model_file} ---")
model = DisasterTweetModel()

if model_file.exists():
    checkpoint = torch.load(model_file, map_location=torch.device('cpu'))
    state_dict = checkpoint['state_dict'] if 'state_dict' in checkpoint else checkpoint
    model.load_state_dict(state_dict)
    print("✅ Model weights loaded.")
else:
    print(f"⚠️ Model not found at {model_file}. Using random weights (Safe for testing).")

model.eval()
tokenizer = AutoTokenizer.from_pretrained("google/bert_uncased_L-2_H-128_A-2")

class TweetRequest(BaseModel):
    text: str

@app.post("/predict")
def predict(request: TweetRequest):
    inputs = tokenizer(request.text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    with torch.no_grad():
        logits = model(inputs["input_ids"], inputs["attention_mask"])
        idx = torch.argmax(logits, dim=1).item()

    label = "Disaster 🚨" if idx == 1 else "Not Disaster 😌"
    return {"prediction": label}

# Mount static files (Only if they exist, so tests don't crash)
if static_path.exists():
    app.mount("/", StaticFiles(directory=str(static_path), html=True), name="static")
