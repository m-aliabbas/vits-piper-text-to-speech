# 🗣️ Piper TTS API – OpenAI Style

This is a simple and developer-friendly **Text-to-Speech API** that wraps [Piper TTS](https://github.com/rhasspy/piper) models using `sherpa-onnx` — and serves them via a **FastAPI** server that mimics OpenAI's `/v1/audio/speech` format.

Yeah, it's like OpenAI... but local, fast, and free.

---

## 🚀 What It Does

You send:

```json
{
  "model": "tts-1",
  "input": "Hello, this is Piper TTS speaking.",
  "voice": "alan_medium",
  "speed": 1.0
}
```

And you get:

* A clean `audio/wav` file with your spoken text.
* Just like OpenAI's TTS — but running 100% on your machine or server.

---

## 🧠 Supported Voices

You don’t need to remember full Hugging Face model IDs.

Just use friendly names like:

| Voice Name                     | Description                    |
| ------------------------------ | ------------------------------ |
| `alan_medium`                  | Male UK English (Piper)        |
| `sweetbbak_amy`                | Female UK English (Piper)      |
| `southern_english_male_medium` | Male UK English, southern      |
| `vctk_medium`                  | 109 speaker multi-voice (VCTK) |

➡️ Check `/` or `/v1/audio/voices` for the full list.

---

## 🛠️ How to Run

### 1. Clone the repo

```bash
git clone https://github.com/yourname/piper-tts-api.git
cd piper-tts-api
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

> Requirements include: `fastapi`, `uvicorn`, `soundfile`, `huggingface_hub`, `sherpa-onnx`

### 3. Run the API

```bash
uvicorn main:app --reload
```

---

## 🎧 Example Request

```bash
curl -X POST http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{
        "model": "tts-1",
        "input": "Hey there! This is a test of the Piper TTS system.",
        "voice": "alan_medium",
        "speed": 1.0
      }' --output piper_output.wav
```

---

## 🧪 Test in Python

```python
import requests

payload = {
    "model": "tts-1",
    "input": "This is a Python test with Piper TTS.",
    "voice": "sweetbbak_amy",
    "speed": 1.0
}

res = requests.post("http://localhost:8000/v1/audio/speech", json=payload)
with open("output.wav", "wb") as f:
    f.write(res.content)
```


---

## 🙌 Credits

* [Piper TTS](https://github.com/rhasspy/piper) – for the models
* [Sherpa ONNX](https://github.com/k2-fsa/sherpa-onnx) – for awesome ONNX inference
* [FastAPI](https://fastapi.tiangolo.com/) – because it's fast and lovely
* Muhammad Ali Abbas Sr. ML Engineer Idrak Ai Ltd. 

