import streamlit as st
from models.llm import get_response
from models.image import process_image
from models.audio import process_audio
from models.language import translate_text
from models.conversation  import save_message, get_context
from PIL import Image

def main():
    # Streamlit UI
    st.title("🧠 Chatbot de Psicología")
    st.write("Este chatbot puede responder a tus preguntas sobre psicología, analizar imágenes y transcribir audio.")

    # Entrada de texto
    input_text = st.text_area("Escribe tu pregunta aquí:")

    # Entrada de imagen
    uploaded_image = st.file_uploader("Sube una imagen", type=["jpg", "png", "jpeg"])

    # Entrada de audio
    uploaded_audio = st.file_uploader("Sube un archivo de audio", type=["wav", "mp3", "m4a"])

    # Selector de idioma
    language = st.selectbox("Idioma de respuesta", ["es", "en"])

    if st.button("Enviar"):
        context = get_context()
        response = ""

        if input_text:
            # Traducir al inglés si el idioma es español
            if language == 'en':
                input_text = translate_text(input_text, target_language='en')
            response = get_response(input_text, context)
            # Traducir al español si la respuesta debe estar en español
            if language == 'es':
                response = translate_text(response, target_language='es')
            save_message(input_text, response)

        if uploaded_image:
            image = Image.open(uploaded_image)
            image_response = process_image(image)
            response += f"\n\n{image_response}"

        if uploaded_audio:
            audio_response = process_audio(uploaded_audio)
            response += f"\n\nTranscripción de audio: {audio_response}"

        st.write(response)

if __name__ == "__main__":
    main()