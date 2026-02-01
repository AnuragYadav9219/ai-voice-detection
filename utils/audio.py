import base64
import io
import librosa
import requests

def decode_base64_audio(base64_audio: str):
    audio_bytes = base64.b64decode(base64_audio)
    audio_buffer = io.BytesIO(audio_bytes)
    y, sr = librosa.load(audio_buffer, sr=None)
    return y, sr

def load_audio_from_url(url: str):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    audio_bytes = io.BytesIO(response.content)
    y, sr = librosa.load(audio_bytes, sr=None)
    return y, sr