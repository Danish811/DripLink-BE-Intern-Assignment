import os
import time
from typing import Any, Dict

from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


_LANGUAGE_MAP = {
    "english": "en",
    "hindi": "hi",
    "urdu": "ur",
    "tamil": "ta",
    "telugu": "te",
    "bengali": "bn",
    "marathi": "mr",
    "kannada": "kn",
    "malayalam": "ml",
    "gujarati": "gu",
    "punjabi": "pa",
}


def _normalize_code(text: str | None) -> str | None:
    if not text:
        return None
    raw = text.strip().lower().strip('.,:;!"\'')
    # If already iso-639-1
    if len(raw) in (2, 3) and raw.isalpha():
        return raw
    return _LANGUAGE_MAP.get(raw, None)


def detect_language_gemini(audio_file_path: str) -> Dict[str, Any]:
    provider = "Google Gemini"
    start_time = time.time()
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

        genai.configure(api_key=api_key)

        uploaded = genai.upload_file(path=audio_file_path)
        prompt = (
            "Identify the primary spoken language in the audio. "
            "Reply with ONLY the ISO-639-1 code (e.g., en, hi, ta, te, bn, ur, mr, kn, ml, gu, pa)."
        )
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([uploaded, prompt])
        text = (getattr(response, "text", "") or "").strip()
        code = _normalize_code(text)

        estimated_cost = {
            "tokens": getattr(getattr(response, "usage_metadata", object()), "tokens", 0),
            "usd": 0.0,
        }
        status = "success" if code else "failure"
        return {
            "provider": provider,
            "language": code,
            "time_taken": round(time.time() - start_time, 4),
            "estimated_cost": estimated_cost,
            "status": status,
            "error_message": None if status == "success" else f"Unclear response: {text[:50]}",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "provider": provider,
            "language": None,
            "time_taken": round(time.time() - start_time, 4),
            "estimated_cost": {"tokens": 0, "usd": 0.0},
            "status": "failure",
            "error_message": str(exc),
        }