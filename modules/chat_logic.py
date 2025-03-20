from modules.settings import client

def create_system_prompt(language):
    prompts = {
        "es": "Eres PsicoChat, un asistente especializado en psicología y salud mental...",
        "en": "You are PsicoChat, an assistant specialized in psychology and mental health...",
        "fr": "Vous êtes PsicoChat, un assistant spécialisé en psychologie et santé mentale..."
    }
    return prompts.get(language, prompts["es"])

def generate_response(prompt, history, pdf_context, mp3_context, image_context, video_context, language):
    system_prompt = create_system_prompt(language)
    formatted_prompt = f"""
    <|system|>
    {system_prompt}

    Contexto adicional (PDF): {pdf_context}
    Contexto adicional (MP3): {mp3_context}
    Contexto adicional (Imagen): {image_context}
    Contexto adicional (Video): {video_context}

    <|user|>
    {history}
    Pregunta actual: {prompt}
    <|assistant|>
    """
    return formatted_prompt
