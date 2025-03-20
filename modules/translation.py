from langdetect import detect
from googletrans import Translator

def translate_text(text, target_lang="es"):
    try:
        translator = Translator()
        detected_lang = detect(text)
        if detected_lang != target_lang:
            return translator.translate(text, src=detected_lang, dest=target_lang).text
        return text
    except Exception as e:
        return f"Error: {e}"
