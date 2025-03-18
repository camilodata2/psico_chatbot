import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_community.llms import HuggingFacePipeline
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from config import ROBUST_CONVERSATION_MODEL
from utils.logger import logger
from models.language import translate_tex, detect_language

def get_memory():
    """
    Inicializa la memoria utilizando ChromaDB y embeddings de Hugging Face.
    Se usa para almacenar y recuperar información de contexto de la conversación.
    """
    try:
        logger.info("Inicializando memoria con ChromaDB...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        vectorstore = Chroma(collection_name="chat_history", embedding_function=embeddings)
        memory = VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever())
        logger.info("Memoria inicializada correctamente.")
        return memory
    except Exception as e:
        logger.error("Error inicializando memoria: %s", e)
        return None

def get_llm(model_size: str = "medium"):
    """
    Loads the DialoGPT model and tokenizer.

    Parameters:
        model_size (str): Model variant to use ("small", "medium", "large"). Default is "medium".

    Returns:
        tuple: (tokenizer, model) if successful, otherwise None.
    """
    try:
        print('I enter the get_llm function')
        logger.info("Loading DialoGPT-%s model...")
        model_name = f"microsoft/DialoGPT-{model_size}"
        tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True, force_download=True)
        model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16, force_download=True)
        return tokenizer, model
    except Exception as e:
        logger.error("Error en generación de respuesta: %s", e)
        return None, None


def generate_response(input_text):
    """
    Generates a chatbot response using DialoGPT.

    Parameters:
        input_text (str): The user input message.

    Returns:
        str: The chatbot response.
    """
    try:
        logger.info("Generando respuesta para la consulta del usuario.")
        print('I enter the generate_response function')
        tokenizer, model = get_llm()
        if tokenizer is None or model is None:
            return "Error: Model not loaded."
        print('I gao the model and the tokenizer')
        if detect_language(input_text) != 'en':
            input_text = translate_tex(input_text, dest_language='en')

        memory = get_memory()
        if memory is None:
            context = ""
        else:
            logger.info("Recuperando contexto desde ChromaDB...")
            retrieved_docs = memory.retriever.invoke(input_text)
            if retrieved_docs:
                context = "\n".join([doc.page_content for doc in retrieved_docs])
                context = translate_tex(context)
                logger.info("Contexto recuperado exitosamente.")
            else:
                context = ""
                logger.info("No se recuperó contexto adicional de ChromaDB.")

        if context:
            prompt = f"""Use the next context to answer accurately:\n {context}\n New Prompt: {input_text}"""
                
        else:
            prompt = input_text

        logger.info("Generando respuesta utilizando el modelo robusto.")
        print('I am about to answer')
        input_ids = tokenizer.encode(prompt + tokenizer.eos_token, return_tensors="pt")

        # Create attention mask
        attention_mask = torch.ones(input_ids.shape, dtype=torch.long)

        # Generate response with explicit attention mask
        response_ids = model.generate(
            input_ids, 
            attention_mask=attention_mask, 
            pad_token_id=tokenizer.eos_token_id
        )

        # Decode and return the response
        response_text = tokenizer.decode(response_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

        response_text = translate_tex(response_text, 'es')
        
        return response_text

    except Exception as e:
        logger.error("Error en generación de respuesta: %s", e)
        return "Ocurrió un error al generar la respuesta."
