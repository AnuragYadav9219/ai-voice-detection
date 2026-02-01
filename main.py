from fastapi import FastAPI, Header, HTTPException, Body
from fastapi.responses import JSONResponse
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


@app.api_route("/honeypot", methods=["GET", "POST"])
async def honeypot(
    payload: dict = Body(default={}),
    x_api_key: str | None = Header(default=None, alias="x-api-key"),
):
    if x_api_key != API_KEY:
        return JSONResponse(status_code=401, content={"status": "unauthorized"})

    return JSONResponse(status_code=200, content={"status": "ok"})