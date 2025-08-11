
# Language Detection Service

This service detects the spoken language in an audio file by integrating with multiple AI providers.

## Setup

1. **Install dependencies:**

   ```bash
   uv pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   Create a `.env` file in the root of the project and add the following:

   ```
   OPENAI_API_KEY="your_openai_api_key"
   GEMINI_API_KEY="your_gemini_api_key"
   ```

## Usage

1. **Run the application:**

   ```bash
   python main.py
   ```

2. **Send a request to the API:**

   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{
       "audio_file_path": "/path/to/your/audio/file.mp3",
       "ground_truth_language": "en"
   }' http://localhost:8000/detect/language
   ```
