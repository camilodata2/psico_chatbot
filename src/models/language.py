from langdetect import detect
from transformers import pipeline
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

def translate_text(text, target_language="en"):
    """
    Traduce el texto al idioma deseado utilizando un modelo de traducción de Hugging Face.
    Si el texto ya está en el idioma de destino, se retorna sin cambios.
    """
    try:
        logger.info("Iniciando traducción de texto.")
        source_language = detect_language(text)
        if source_language == target_language:
            logger.info("El texto ya se encuentra en el idioma destino.")
            return text
        model_name = f"Helsinki-NLP/opus-mt-{source_language}-{target_language}"
        translator = pipeline("translation", model=model_name)
        translation = translator(text)[0]['translation_text']
        logger.info("Traducción completada.")
        return translation
    except Exception as e:
        logger.error("Error en traducción de texto: %s", e)
        return text
