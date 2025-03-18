from langdetect import detect
from deep_translator import GoogleTranslator
from utils.logger import logger

def detect_language(text):
    """
    Detecta el idioma de un texto.
    """
    try:
        logger.info("Detectando idioma para el texto proporcionado.")
        lang = detect(text)
        logger.info("Idioma detectado: %s", lang)
        return lang
    except Exception as e:
        logger.error("Error detectando idioma: %s", e)
        return "en"

def translate_tex(text, dest_language="es"):
    """
    Traduce un texto al idioma especificado.

    Parámetros:
        texto (str): Texto a traducir.
        idioma_destino (str): Código del idioma destino (ej. 'es' para español, 'en' para inglés).

    Retorna:
        str: Texto traducido o un mensaje de error si falla la traducción.
    """
    try:
        source_language = detect_language(text)
        translator = GoogleTranslator(source=source_language, target=dest_language)
        return translator.translate(text)
    except Exception as e:
        print(f"Error: {type(e).__name__} - {str(e)}")
        return text
