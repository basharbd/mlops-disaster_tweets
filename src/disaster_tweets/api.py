import json
import time
from fastapi import FastAPI, BackgroundTasks
from google.cloud import storage
from pydantic import BaseModel

app = FastAPI()


BUCKET_NAME = "dt-bucket-bashar-2026"

class PredictRequest(BaseModel):
    text: str

class PredictResponse(BaseModel):
    text: str
    prediction: str
    class_id: int

def upload_to_bucket(data: dict):
  
    try:
        print(f">>> UPLOAD START: {BUCKET_NAME}")
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(f"predictions/pred_{int(time.time())}.json")
        blob.upload_from_string(json.dumps(data), content_type="application/json")
        print(">>> UPLOAD SUCCESS!")
    except Exception as e:
        print(f">>> UPLOAD FAILED: {e}")

@app.get("/")
def root():
    return {"status": "System Alive & Running!"}

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest, background_tasks: BackgroundTasks):
    response_data = {
        "text": request.text,
        "prediction": "Disaster 🚨 (Saved to Cloud)",
        "class_id": 1
    }
   
    background_tasks.add_task(upload_to_bucket, response_data)
    return PredictResponse(**response_data)
