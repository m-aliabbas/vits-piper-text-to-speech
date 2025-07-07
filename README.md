# 🗣️ Piper TTS API – OpenAI Style

This is a FastAPI server that runs **Piper TTS models** using `sherpa-onnx`, and gives you an **OpenAI-style text-to-speech API**. Send text and a voice ID — get back a WAV file.

---

## 🚀 Features

- 🧠 Fast, local TTS using Piper + ONNX
- 🧪 OpenAI-compatible endpoint (`/v1/audio/speech`)
- 🎙️ Friendly voice names (no more long repo IDs)
- ⚡ Supports speed control + speaker counts

---

## 📦 API Endpoints

### `POST /v1/audio/speech`

Convert text to speech using a Piper voice.

**Request:**
```json
{
  "model": "tts-1",
  "input": "Hello world!",
  "voice": "alan_medium",
  "speed": 1.0
}
````

**Response:**

* `audio/wav` file (spoken audio)
* Headers:

  * `X-Audio-Duration`
  * `X-RTF` (Real-time factor)

---

### `GET /v1/voices`

Get all available voice IDs:

```json
{
  "voices": [
    "alan_medium",
    "sweetbbak_amy",
    "southern_english_male_medium",
    ...
  ]
}
```

Use these as the `voice` field in `/v1/audio/speech`.

---

### `GET /v1/voices/{voice}/speakers`

Get number of speakers supported by a voice:

**Example:**

```http
GET /v1/voices/vctk_medium/speakers
```

**Response:**

```json
{
  "num_speakers": 109
}
```

---

## 🔧 How to Run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🎧 Example cURL Usage

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "tts-1",
        "input": "This is a test of Piper TTS",
        "voice": "alan_medium",
        "speed": 1.0
      }' --output piper_speech.wav
```

---

## 🙌 Credits

* [Piper TTS](https://github.com/rhasspy/piper)
* [Sherpa ONNX](https://github.com/k2-fsa/sherpa-onnx)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Muhammad Ali Abbas](https://m-aliabbas.vercel.app/)