import io
from transformers import pipeline

AUDIO_MODEL = "openai/whisper-large-v2"
whisper = pipeline("automatic-speech-recognition", model=AUDIO_MODEL)

def process_audio(audio):
    audio_bytes = io.BytesIO(audio.read())
    transcript = whisper(audio_bytes)["text"]
    return transcript