from transformers import AutoTokenizer, AutoModelForCausalLM
from huggingface_hub import login
import os
from dotenv import load_dotenv

# Cargar API Key desde la variable de entorno
load_dotenv()
hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(hf_token)
else:
    raise ValueError("La variable de entorno HF_TOKEN no está definida")

MODEL_NAME = "tiiuae/falcon-40b-instruct"
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

def get_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response