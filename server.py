from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from pydantic import BaseModel
import soundfile as sf
import uuid
import os
import time

from model import get_pretrained_model, friendly_model_names, get_available_speakers

app = FastAPI(title="OpenAI-Compatible Sherpa Piper TTS")


class OpenAITTSRequest(BaseModel):
    model: str  # OpenAI-style model field (ignored internally)
    input: str  # Text to synthesize
    voice: str  # Friendly name like "alan_medium"
    speed: float = 1.0  # Speech speed factor


@app.get("/", summary="API Info", tags=["General"])
def index():
    """
    Returns a basic welcome message and available voice list.
    """
    return {
        "message": "OpenAI-compatible Piper TTS server is running.",
        "example_endpoint": "/v1/audio/speech",
        "available_voices": list(friendly_model_names.keys()),
    }


@app.post("/v1/audio/speech", summary="Synthesize Speech", tags=["Speech"])
def tts_openai_format(req: OpenAITTSRequest):
    """
    Convert input text to speech using the selected Piper voice.

    Request Body:
    - model: Just use "tts-1"
    - input: The text to synthesize
    - voice: Voice ID (see /v1/voices)
    - speed: Optional speed factor (default = 1.0)

    Returns:
    - audio/wav file containing generated speech
    """
    try:
        voice = req.voice.strip()

        if voice not in friendly_model_names:
            raise HTTPException(status_code=404, detail=f"Unknown voice: {voice}")

        repo_id = friendly_model_names[voice]
        tts = get_pretrained_model(repo_id, req.speed)

        start = time.time()
        audio = tts.generate(req.input, sid=0)
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


@app.get("/v1/voices", summary="List Available Voices", tags=["Voices"])
def get_available_voices():
    """
    Returns a list of all available friendly voice names.
    Use these as `voice` in `/v1/audio/speech`.
    """
    return {
        "voices": list(friendly_model_names.keys())
    }


@app.get("/v1/voices/{voice_id}/speakers", summary="Get Number of Speakers", tags=["Voices"])
def get_speakers(voice_id: str):
    """
    Returns the number of available speakers for a given voice.

    Path Param:
    - voice_id: One of the voice names from `/v1/voices`

    Returns:
    - Number of supported speakers
    """
    try:
        speakers = get_available_speakers(voice_id)
        return {"num_speakers": speakers}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
