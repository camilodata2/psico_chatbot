# models/image.py
from transformers import pipeline
from PIL import Image
from config import IMAGE_CAPTION_MODEL

# Inicializamos el pipeline de captioning
caption_pipeline = pipeline("image-to-text", model=IMAGE_CAPTION_MODEL)

def process_image(image_file):
    """
    Procesa la imagen y devuelve una descripción generada.
    """
    image = Image.open(image_file)
    result = caption_pipeline(image)
    return result[0]['generated_text']
