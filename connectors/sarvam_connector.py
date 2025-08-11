import os
import time
from typing import Any, Dict
from sarvamai import SarvamAI 
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("SARVAM_API_KEY")

def _from_sarvam(response: Any) -> str | None:
    try:
        if hasattr(response, "results") and response.results:
            first = response.results[0]
            code = getattr(first, "language_code", None)
            if code:
                return str(code).lower()
    except Exception:
        return None
    return None


def detect_language_sarvam(audio_file_path: str) -> Dict[str, Any]:
    provider = "Sarvam AI"
    start_time = time.time()
    
    try:
        if not api_key or SarvamAI is None:
            raise RuntimeError("Sarvam SDK unavailable or SARVAM_API_KEY not set")

        client = SarvamAI(api_subscription_key=api_key)
        with open(audio_file_path, "rb") as audio_file:
            response = client.speech_to_text.transcribe(
                file=audio_file,
                model="saarika:v2.5",
                language_code="unknown"
            )
        print(response)
        code = _from_sarvam(response)
        status = "success" if code else "failure"
        return {
            "provider": provider,
            "language": code,
            "time_taken": round(time.time() - start_time, 4),
            "estimated_cost": {"tokens": 0, "usd": 0.0},
            "status": status,
            "error_message": None if status == "success" else "Language not present in response",
        }
    except Exception as exc:  
        return {
            "provider": provider,
            "language": None,
            "time_taken": round(time.time() - start_time, 4),
            "estimated_cost": {"tokens": 0, "usd": 0.0},
            "status": "failure",
            "error_message": str(exc),
        }