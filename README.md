# 🎙️ Language Detection Service

A FastAPI-based service that detects the spoken language in an audio file by integrating with multiple AI providers, including:

* **Google Gemini**
* **ElevenLabs**
* **Sarvam AI**
* **OpenAI** (placeholder implementation)

The service runs all available connectors in parallel and returns their detection results along with processing time and cost estimates.

---

## 📂 Project Structure

```
Driplink-be-intern-assignment/
├── main.py                  # Entry point for running the FastAPI app
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── api/
│   └── main.py               # FastAPI routes and request handling
├── connectors/               # Language detection integrations
│   ├── gemini_connector.py
│   ├── elevenlabs_connector.py
│   ├── sarvam_connector.py
│   └── openai_connector.py
└── coordinator/
    └── coordinator.py        # Runs all providers in parallel and aggregates results
```

---

## 🚀 Features

✅ Detects language from audio using multiple AI providers.
✅ Returns **ISO-639-1** language codes (e.g., `en`, `hi`, `ta`).
✅ Provides **execution time** and **estimated cost** per provider.
✅ Runs all providers **concurrently** for faster results.
✅ Easy-to-extend architecture for adding more providers.

---

## 🛠 Setup

### 1️⃣ Install Dependencies

We recommend using a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows

pip install -r requirements.txt
```

---

### 2️⃣ Configure Environment Variables

Create a `.env` file in the root directory:

```ini
OPENAI_API_KEY=your_openai_api_key
GEMINI_API_KEY=your_gemini_api_key
SARVAM_API_KEY=your_sarvam_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

> Only the providers with valid API keys will return results. Others will fail gracefully.

---

### 3️⃣ Run the Application

```bash
python main.py
```

The service will start at:

```
http://localhost:8000
```

---

## 📡 API Usage

### **Endpoint**

`POST /detect/language`

### **Request Body**

```json
{
  "audio_file_path": "/path/to/your/audio/file.mp3",
  "ground_truth_language": "en"   // Optional
}
```

### **Response Example**

```json
[
  {
    "provider": "Google Gemini",
    "language": "en",
    "time_taken": 1.2345,
    "estimated_cost": { "tokens": 100, "usd": 0.002 },
    "status": "success",
    "error_message": null
  },
  {
    "provider": "Sarvam AI",
    "language": "hi",
    "time_taken": 0.9542,
    "estimated_cost": { "tokens": 0, "usd": 0.0 },
    "status": "success",
    "error_message": null
  },
  ...
]
```

---

## 🧪 Running Tests

If you have test files in `tests/`, you can run them using:

```bash
pytest
```

---

## 🔌 Connectors

| Provider      | File                                 | Notes                                                              |
| ------------- | ------------------------------------ | ------------------------------------------------------------------ |
| Google Gemini | `connectors/gemini_connector.py`     | Uses `google-generativeai` for audio analysis.                     |
| ElevenLabs    | `connectors/elevenlabs_connector.py` | Uses `ElevenLabs` API for speech-to-text and language detection.   |
| Sarvam AI     | `connectors/sarvam_connector.py`     | Uses `sarvamai` SDK for transcription and language detection.      |
| OpenAI        | `connectors/openai_connector.py`     | Currently a placeholder, returns provided `ground_truth_language`. |

---

## 📌 Notes

* The **OpenAI connector** is currently mocked and does not perform actual detection.
* This project is designed for **local development** but can be deployed to cloud platforms.
* API keys must be valid for the respective connectors to work.

---
