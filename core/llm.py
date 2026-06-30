import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"

def chat_json(system: str, user: str) -> dict:
    """Call the model and parse a guaranteed-JSON response."""
    resp = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
        temperature=0.4,
    )
    return json.loads(resp.choices[0].message.content)

def transcribe_audio(audio_file) -> str:
    """Transcribes audio using OpenAI Whisper API."""
    try:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
        return transcript.text
    except Exception as e:
        return f"Transcription error: {str(e)}"