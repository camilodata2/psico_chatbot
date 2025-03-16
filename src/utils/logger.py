import logging

def setup_logger():
    # Configura el logger
    logger = logging.getLogger("chatbot_logger")
    logger.setLevel(logging.INFO)

    # Crear un manejador para escribir en un archivo
    fh = logging.FileHandler("user_interactions.log")
    fh.setLevel(logging.INFO)

    # Definir el formato de los mensajes
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    # Evitar agregar múltiples handlers en caso de recarga del módulo
    if not logger.handlers:
        logger.addHandler(fh)
    
    return logger

logger = setup_logger()

def log_interaction(user_input, chatbot_response):
    """
    Registra la interacción: entrada del usuario y respuesta del chatbot.
    """
    logger.info("User Input: %s; Chatbot Response: %s", user_input, chatbot_response)
