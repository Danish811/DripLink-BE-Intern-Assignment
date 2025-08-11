
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import asyncio
from dotenv import load_dotenv
from coordinator.coordinator import run_language_detection

load_dotenv()

app = FastAPI(title="Language Detection Service")


class DetectLanguageRequest(BaseModel):
    audio_file_path: str
    ground_truth_language: str | None = None


@app.post("/detect/language")
async def detect_language(payload: DetectLanguageRequest):
    if not os.path.exists(payload.audio_file_path):
        raise HTTPException(status_code=400, detail="Audio file not found.")

    results = await run_language_detection(payload.audio_file_path, payload.ground_truth_language)
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
