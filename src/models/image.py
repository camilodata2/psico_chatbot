from transformers import pipeline

IMAGE_MODEL = "openai/clip-vit-large-patch14"
clip = pipeline("image-classification", model=IMAGE_MODEL)

def process_image(image):
    labels = clip(image)
    description = ", ".join([label['label'] for label in labels])
    return f"La imagen contiene: {description}"