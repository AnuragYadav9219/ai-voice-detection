from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from utils.audio import decode_base64_audio
from utils.features import extract_mfcc
from model.classifier import classify

API_KEY = "my-secret-key"

app = FastAPI(title="AI Voice Detection API")


class AudioRequest(BaseModel):
    language: str
    audio_format: str = Field(..., alias="audioFormat")
    audio_base64: str = Field(..., alias="audioBase64")

    class Config:
        allow_population_by_field_name = True


@app.post("/detect")
def detect_voice(
    request: AudioRequest, x_api_key: str = Header(None, alias="x-api-key")
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

    if request.language not in ["en", "hi", "ta", "ml", "te"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    try:
        y, sr = decode_base64_audio(request.audio_base64)
        features = extract_mfcc(y, sr)
        label, confidence = classify(features)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {"result": label, "confidence": confidence}


@app.post("/honeypot")
def honeypot(x_api_key: str = Header(None, alias="x-api-key")):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized access detected")

    return {"status": "ok", "message": "Honeypot endpoint reached successfully"}
