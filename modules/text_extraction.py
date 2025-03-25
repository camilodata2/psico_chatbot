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
    """
    Extrae texto de un archivo PDF.

    Args:
        pdf_file (str): La ruta al archivo PDF del cual se extraerá el texto.

    Returns:
        str: El texto extraído del archivo PDF. Si ocurre un error durante la extracción, 
             se devuelve un mensaje de error con la descripción del problema.
    """
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        return "".join(page.extract_text() or "" for page in reader.pages)
    except Exception as e:
        return f"Error extracting text: {e}"

def extract_text_from_audio(audio_path, language='es'):
    """
    Extrae texto de un archivo de audio utilizando el servicio de reconocimiento de voz de Google.
    Args:
        audio_path (str): La ruta del archivo de audio. Puede ser un archivo .wav o .mp3.
        language (str): El código del idioma para el reconocimiento de voz. Por defecto es 'es' (español).
    Returns:
        str: El texto extraído del audio. En caso de error, devuelve un mensaje de error.
    Raises:
        Exception: Si ocurre un error durante la extracción del texto.
    """
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
    """
    Extrae texto de una imagen utilizando OCR (Reconocimiento Óptico de Caracteres).

    Args:
        image_file (file-like object): Archivo de imagen desde el cual se extraerá el texto.
        lang (str, opcional): Código de idioma para el OCR. El valor predeterminado es "esp" (español).

    Returns:
        str: Texto extraído de la imagen. Si ocurre un error, se devuelve un mensaje de error.
    """
    try:
        image = Image.open(io.BytesIO(image_file.read()))
        return pytesseract.image_to_string(image, lang=lang).strip()
    except Exception as e:
        return f"Error processing image: {e}"

def extract_text_from_video(uploaded_video, audio_language='es'):
    """
    Extrae texto de un video subido.
    Este método toma un video subido, extrae el audio del video y luego
    extrae el texto del audio utilizando un método de reconocimiento de voz.
    Args:
        uploaded_video (FileStorage): El archivo de video subido.
        audio_language (str): El idioma del audio en el video. Por defecto es 'es' (español).
    Returns:
        str: El texto extraído del audio del video o un mensaje de error si ocurre una excepción.
    """
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
