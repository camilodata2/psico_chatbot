from modules.settings import client

def create_system_prompt(language):

    """
    Genera un mensaje de aviso del sistema basado en el idioma especificado.
        language (str): El código del idioma para el mensaje deseado.
                        Los valores soportados son "es" (español), "en" (inglés) y "fr" (francés).
        str: Un mensaje de aviso del sistema en el idioma especificado.
             Por defecto, devuelve el mensaje en español ("es") si el código de idioma proporcionado no es soportado.
    """
    prompts = {
        "es": "Eres PsicoChat, un asistente especializado en psicología y salud mental...",
        "en": "You are PsicoChat, an assistant specialized in psychology and mental health...",
        "fr": "Vous êtes PsicoChat, un assistant spécialisé en psychologie et santé mentale..."
    }
    return prompts.get(language, prompts["es"])

def generate_response(prompt, history, pdf_context, mp3_context, image_context, video_context, language):
    """"    Genera una respuesta formateada basada en el prompt del usuario y varios contextos adicionales.
    Args:
        prompt (str): La pregunta o solicitud actual del usuario.
        history (str): El historial de conversación previo con el usuario.
        pdf_context (str): Contexto adicional proporcionado por el usuario a través de un archivo PDF.
        mp3_context (str): Contexto adicional proporcionado por el usuario a través de un archivo de audio MP3.
        image_context (str): Contexto adicional proporcionado por el usuario a través de una imagen.
        video_context (str): Contexto adicional proporcionado por el usuario a través de un archivo multimedia o video.
        language (str): El idioma en el que se debe generar la respuesta.
    Returns:
        str: Un string formateado que combina el prompt del sistema, el contexto adicional y la pregunta actual del usuario."""
    system_prompt = create_system_prompt(language)
    formatted_prompt = f"""
    <|system|>
    {system_prompt}

    Contexto adicional proporcionado por el usuario por medio de un archivo pdf: {pdf_context}
    Contexto adicional proporcionado por el usuario por medio de un archivo de audio mp3: {mp3_context}
    Contexto adicional proporcionado por el usuario por medio de una imagen: {image_context}
    Contexto adicional proporcionado por el usuario por medio de un archivo multimedia o video: {video_context}

    <|user|>
    {history}
    Pregunta actual: {prompt}
    <|assistant|>
    """
    return formatted_prompt
