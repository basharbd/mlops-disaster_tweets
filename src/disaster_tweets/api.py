from fastapi import FastAPI
from pydantic import BaseModel
import torch
from transformers import AutoTokenizer
from disaster_tweets.models import DisasterTweetModel

app = FastAPI()

# 1. Define what valid input looks like
class TweetRequest(BaseModel):
    text: str

# 2. Load the Model and Tokenizer
# We load these once when the server starts so it's fast
print("Loading model...")
model = DisasterTweetModel()
model.eval()  # Set model to evaluation mode (no training)
tokenizer = AutoTokenizer.from_pretrained("google/bert_uncased_L-2_H-128_A-2")  # Use a small BERT for speed
print("Model loaded!")

@app.get("/")
def read_root():
    return {"message": "Disaster Tweet Classifier is Ready!"}

@app.post("/predict")
def predict(request: TweetRequest):
    # A. Tokenize the incoming text
    inputs = tokenizer(
        request.text,
        return_tensors="pt",
        padding=True,
        truncation=True,
        max_length=128
    )

    # B. Run the model
    with torch.no_grad():
        # Forward pass
        logits = model(inputs["input_ids"], inputs["attention_mask"])
        # Get the class (0 or 1)
        prediction_index = torch.argmax(logits, dim=1).item()

    # C. Convert to readable label
    label = "Disaster 🚨" if prediction_index == 1 else "Not Disaster 😌"

    return {
        "text": request.text,
        "prediction": label,
        "class_id": prediction_index
    }
