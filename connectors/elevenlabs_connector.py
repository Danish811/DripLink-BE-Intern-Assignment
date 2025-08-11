import os
import time
from typing import Any, Dict, Optional

from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

def detect_language_elevenlabs(audio_file_path: str) -> Dict[str, Any]:
    provider = "ElevenLabs"
    start_time = time.time()
    
    elevenlabs = ElevenLabs(
       api_key=api_key
    )
    try:
        with open(audio_file_path, "rb") as file:
            audio_data = BytesIO(file.read())
        transcription = elevenlabs.speech_to_text.convert(
            file=audio_data,
            model_id="scribe_v1",
            # language_code="None", 
        )
        print(transcription.language_code)
        code = transcription.language_code
        estimated_cost = {
                "tokens": getattr(getattr(transcription, "usage_metadata", object()), "tokens", 0),
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
    except Exception as exc:  
        return {
            "provider": provider,
            "language": None,
            "time_taken": round(time.time() - start_time, 4),
            "estimated_cost": {"tokens": 0, "usd": 0.0},
            "status": "failure",
            "error_message": str(exc),
        }

#detect_language_elevenlabs("C:/Users/danis/Downloads/Automated Coding/language_detection_service/tests/hi_test.mp3")