from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import soundfile as sf
import uuid
import os
import time

from model import get_pretrained_model, friendly_model_names,get_available_speakers

app = FastAPI(title="OpenAI-Compatible Sherpa TTS")


class OpenAITTSRequest(BaseModel):
    model: str  # e.g., "tts-1"
    input: str
    voice: str  # e.g., "alan_medium"
    speed: float = 1.0


@app.get("/")
def index():
    return {
        "message": "OpenAI-compatible TTS server is running.",
        "example_endpoint": "/v1/audio/speech",
        "available_voices": list(friendly_model_names.keys()),
    }


@app.post("/v1/audio/speech")
def tts_openai_format(req: OpenAITTSRequest):
    try:
        voice = req.voice.strip()

        if voice not in friendly_model_names:
            raise HTTPException(status_code=404, detail=f"Unknown voice: {voice}")

        repo_id = friendly_model_names[voice]
        tts = get_pretrained_model(repo_id, req.speed)

        start = time.time()
        audio = tts.generate(req.input, sid=0)  # speaker_id=0 by default
        end = time.time()

        if len(audio.samples) == 0:
            raise HTTPException(status_code=500, detail="Audio generation failed")

        duration = len(audio.samples) / audio.sample_rate
        rtf = (end - start) / duration

        filename = f"/tmp/{uuid.uuid4().hex}.wav"
        sf.write(filename, audio.samples, samplerate=audio.sample_rate, subtype="PCM_16")

        return FileResponse(
            path=filename,
            media_type="audio/wav",
            filename="speech.wav",
            headers={
                "X-Audio-Duration": f"{duration:.3f}",
                "X-RTF": f"{rtf:.3f}"
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/voices")
def get_available_voices():
    """
    Returns a list of available voices.
    """
    return {
        "voices": list(friendly_model_names.keys())
    }
@app.get("/v1/voices/{voice_id}/speakers")
def get_speakers(voice_id: str):
    """
    Returns a list of available speakers for a given voice.
    """
    try:
        speakers = get_available_speakers(voice_id)
        return {"num_speakers": speakers}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
        return {"num_speakers": 1} 