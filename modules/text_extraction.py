import io
import os
import tempfile
import pytesseract
import PyPDF2
import ffmpeg
import speech_recognition as sr
from pydub import AudioSegment
from PIL import Image

def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"Error extracting text: {e}"

def extract_text_from_audio(audio_path, language='es'):
    try:
        if not audio_path.lower().endswith(".wav"):
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                AudioSegment.from_mp3(audio_path).export(temp_wav.name, format="wav")
                audio_path = temp_wav.name

        recognizer = sr.Recognizer()
        with sr.AudioFile(audio_path) as source:
            audio_data = recognizer.record(source)
        return recognizer.recognize_google(audio_data, language=language)
    except Exception as e:
        return f"Error extracting text: {e}"

def extract_text_from_image(image_file, lang="esp"):
    try:
        image = Image.open(io.BytesIO(image_file.read()))
        return pytesseract.image_to_string(image, lang=lang).strip()
    except Exception as e:
        return f"Error processing image: {e}"

def extract_text_from_video(uploaded_video, audio_language='es'):
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_video.read())
            video_path = temp_video.name

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_path = temp_audio.name

        ffmpeg.input(video_path).output(audio_path, format="wav").run(overwrite_output=True)
        return extract_text_from_audio(audio_path, audio_language)
    except Exception as e:
        return f"Error processing video: {e}"
