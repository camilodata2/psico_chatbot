from langdetect import detect
from googletrans import Translator

def translate_text(text, target_lang="es"):
    """
    Traduce el texto dado al idioma objetivo especificado.

    Args:
        text (str): El texto que se desea traducir.
        target_lang (str): El código del idioma objetivo al que se desea traducir el texto. Por defecto es "es" (español).

    Returns:
        str: El texto traducido si la detección del idioma es diferente al idioma objetivo, de lo contrario, devuelve el texto original.
        En caso de error, devuelve un mensaje de error con la descripción del mismo.
    """
    try:
        translator = Translator()
        detected_lang = detect(text)
        if detected_lang != target_lang:
            return translator.translate(text, src=detected_lang, dest=target_lang).text
        return text
    except Exception as e:
        return f"Error: {e}"
