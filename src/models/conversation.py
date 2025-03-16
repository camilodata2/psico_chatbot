from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain.llms import HuggingFacePipeline
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.memory import VectorStoreRetrieverMemory
from config import ROBUST_CONVERSATION_MODEL
from utils.logger import logger
from models.language import translate_text

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

def get_llm():
    """
    Inicializa el modelo robusto para conversación utilizando HuggingFacePipeline a través de LangChain.
    """
    try:
        logger.info("Cargando modelo robusto para conversación...")
        tokenizer = AutoTokenizer.from_pretrained(ROBUST_CONVERSATION_MODEL)
        model = AutoModelForCausalLM.from_pretrained(ROBUST_CONVERSATION_MODEL, device_map="auto")
        hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=512)
        llm = HuggingFacePipeline(pipeline=hf_pipeline)
        logger.info("Modelo robusto cargado correctamente.")
        return llm
    except Exception as e:
        logger.error("Error cargando modelo robusto: %s", e)
        return None

def generate_response(input_text, language="es"):
    """
    Genera una respuesta usando el LLM robusto y utilizando información de contexto extraída desde ChromaDB.
    Si el idioma no es inglés, se traduce la entrada y la respuesta.
    """
    try:
        logger.info("Generando respuesta para la consulta del usuario.")
        if language != "en":
            input_text_en = translate_text(input_text, target_language="en")
            logger.info("Entrada traducida a inglés para procesamiento.")
        else:
            input_text_en = input_text

        llm = get_llm()
        if llm is None:
            return "Error en la generación de respuesta."

        memory = get_memory()
        if memory is None:
            context = "No se encontró información adicional."
        else:
            logger.info("Recuperando contexto desde ChromaDB...")
            retrieved_docs = memory.retriever.get_relevant_documents(input_text_en)
            if retrieved_docs:
                context = "\n".join([doc.page_content for doc in retrieved_docs])
                logger.info("Contexto recuperado exitosamente.")
            else:
                context = "No se encontró información adicional."
                logger.info("No se recuperó contexto adicional de ChromaDB.")

        prompt = (
            f"Utiliza la siguiente información de contexto para responder de manera precisa:\n"
            f"{context}\n\n"
            f"Pregunta: {input_text_en}\n\n"
            f"Respuesta:"
        )

        logger.info("Generando respuesta utilizando el modelo robusto.")
        response_en = llm(prompt)
        logger.info("Respuesta generada por el modelo.")

        if language != "en":
            response = translate_text(response_en, target_language=language)
            logger.info("Respuesta traducida al idioma original.")
        else:
            response = response_en

        return response
    except Exception as e:
        logger.error("Error en generación de respuesta: %s", e)
        return "Ocurrió un error al generar la respuesta."
