from transformers import pipeline
from config import ASR_MODEL

# Inicializamos el pipeline de transcripción
asr_pipeline = pipeline("automatic-speech-recognition", model=ASR_MODEL)

def transcribe_audio(audio_file):
    """
    Transcribe el contenido de un archivo de audio a texto.
    """
    audio_bytes = audio_file.read()
    result = asr_pipeline(audio_bytes)
    return result["text"]
