import streamlit as st
from models.audio import transcribe_audio
from models.image import process_image
from models.language import detect_language
from models.conversation import generate_response
from utils.logger import log_interaction, logger

def main():
    try:
        st.title("Chatbot de Psicología Multimodal")
        st.write("Envía tu consulta en texto, imagen o audio.")

        # Entrada de texto
        user_text = st.text_input("Escribe tu mensaje:")

        # Subida de imagen
        user_image = st.file_uploader("Sube una imagen (jpg, jpeg, png)", type=["jpg", "jpeg", "png"])

        # Subida de audio
        user_audio = st.file_uploader("Sube un audio (wav, mp3, ogg)", type=["wav", "mp3", "ogg"])

        if st.button("Enviar Consulta"):
            combined_input = ""
            
            try:
                if user_text:
                    combined_input += user_text
            except Exception as e:
                logger.error("Error procesando texto: %s", e)

            try:
                if user_image is not None:
                    st.write("Procesando imagen...")
                    image_caption = process_image(user_image)
                    st.write("Descripción de la imagen:", image_caption)
                    combined_input += " " + image_caption
            except Exception as e:
                logger.error("Error procesando imagen: %s", e)

            try:
                if user_audio is not None:
                    st.write("Procesando audio...")
                    audio_text = transcribe_audio(user_audio)
                    st.write("Transcripción de audio:", audio_text)
                    combined_input += " " + audio_text
            except Exception as e:
                logger.error("Error procesando audio: %s", e)

            if combined_input.strip():
                st.write("Entrada combinada:", combined_input)
                lang = detect_language(combined_input)
                st.write("Idioma detectado:", lang)
                st.write("Generando respuesta del chatbot robusto...")
                response = generate_response(combined_input, language=lang)
                st.write("Respuesta del Chatbot:")
                st.write(response)
                
                log_interaction(combined_input, response)
                logger.info("Interacción registrada en el log.")
            else:
                st.write("Por favor, ingresa algún contenido para procesar.")
    except Exception as e:
        logger.error("Error en la aplicación principal: %s", e)
        st.write("Ocurrió un error en la aplicación.")

if __name__ == "__main__":
    main()
