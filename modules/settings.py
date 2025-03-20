import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

# Cargar variables de entorno
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Configurar modelo de Hugging Face
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"
client = InferenceClient(model=MODEL, token=HUGGINGFACE_API_KEY)
