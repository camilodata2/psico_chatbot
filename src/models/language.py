from transformers import pipeline

TRANSLATE_MODEL = "Helsinki-NLP/opus-mt-en-es"
translator = pipeline("translation", model=TRANSLATE_MODEL)

def translate_text(text, target_language):
    if target_language == "en":
        translated = translator(text, src_lang="es", tgt_lang="en")[0]['translation_text']
    else:
        translated = translator(text, src_lang="en", tgt_lang="es")[0]['translation_text']
    return translated