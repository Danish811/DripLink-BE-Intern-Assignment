
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Callable, Optional

from connectors.gemini_connector import detect_language_gemini
from connectors.sarvam_connector import detect_language_sarvam
from connectors.elevenlabs_connector import detect_language_elevenlabs
from connectors.openai_connector import detect_language_openai


def _wrap_call(fn: Callable[..., Dict[str, Any]], audio_file_path: str, kwargs: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    try:
        kwargs = kwargs or {}
        return fn(audio_file_path, **kwargs)
    except Exception as exc: 
        return {
            "provider": fn.__name__,
            "language": None,
            "time_taken": 0.0,
            "estimated_cost": {"tokens": 0, "usd": 0.0},
            "status": "failure",
            "error_message": str(exc),
        }


async def run_language_detection(audio_file_path: str, ground_truth_language: Optional[str] = None) -> List[Dict[str, Any]]:
    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=4) as pool:
        tasks = [
            loop.run_in_executor(pool, _wrap_call, detect_language_gemini, audio_file_path, None),
            loop.run_in_executor(pool, _wrap_call, detect_language_sarvam, audio_file_path, None),
            loop.run_in_executor(pool, _wrap_call, detect_language_elevenlabs, audio_file_path, None),
            loop.run_in_executor(pool, _wrap_call, detect_language_openai, audio_file_path, {"ground_truth_language": ground_truth_language}),
        ]
        results = await asyncio.gather(*tasks)
    return results
