import os
import io
import tempfile
import time
import pytesseract
import ffmpeg

from dotenv import load_dotenv
from huggingface_hub import InferenceClient
import streamlit as st
import PyPDF2  # Para extraer texto de PDFs
import speech_recognition as sr
from pydub import AudioSegment
from langdetect import detect
from googletrans import Translator
from PIL import Image

# Cargar variables de entorno
load_dotenv()
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

# Configurar el modelo - Usamos un modelo más adecuado para conversaciones y multilingüe
MODEL = "mistralai/Mistral-7B-Instruct-v0.2"  # Mejor para generación de texto y multilingüe

# Inicializar el cliente de Hugging Face
client = InferenceClient(model=MODEL, token=HUGGINGFACE_API_KEY)

# Configuración de la página
st.set_page_config(
    page_title="PsicoChat - Asistente de Psicología",
    page_icon="🧠",
    layout="wide"
)

# Estilos CSS personalizados
st.markdown("""
            <style>
            .main { background-color: #f5f5f5; }
            .stApp { max-width: 1200px; margin: 0 auto; }
            .chat-container { background-color: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .user-message { background-color: #e6f7ff; border-radius: 15px; padding: 10px 15px; margin: 5px 0; }
            .assistant-message { background-color: #f0f2f5; border-radius: 15px; padding: 10px 15px; margin: 5px 0; }
            .disclaimer { font-size: 0.8em; color: #666; font-style: italic; }
            </style>
        """, unsafe_allow_html=True)

def translate_text(text, target_lang="es"):
    """
    Detects the language of the given text and translates it into the target language.
    
    Args:
        text (str): The input text.
        target_lang (str): The language code to translate the text into (default: "es" for Spanish).
    
    Returns:
        str: Translated text.
    """
    try:
        translator = Translator()
        detected_lang = detect(text)

        if detected_lang != target_lang:
            translated_text = translator.translate(text, src=detected_lang, dest=target_lang).text
            return translated_text
        return text  # If already in target language, return as is

    except Exception as e:
        return f"Error: {e}"

# Función para extraer texto de PDFs
def extract_text_from_pdf(pdf_file):
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""

        return text

    except Exception as e:
        print(f"Error extracting text: {e}")
        return None

def extract_text_from_audio(audio_path, audio_language='es'):
    try:
        # Check if the file is already in WAV format
        if audio_path.lower().endswith(".wav"):
            wav_path = audio_path  # Use the WAV file directly
        else:
            # Convert MP3 to WAV using a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
                audio = AudioSegment.from_mp3(audio_path)
                audio.export(temp_wav.name, format="wav")
                wav_path = temp_wav.name

        # Speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language=audio_language)

        # Delete the temporary file if conversion was done
        if audio_path.lower().endswith(".mp3"):
            os.remove(wav_path)

        return text

    except Exception as e:
        return f"Error extracting text: {e}"

# Extract text from a image
def extract_text_from_image(image_file, lang="esp"):
    """
    Extracts text from an uploaded image file using Tesseract OCR.

    Args:
        image_file (BytesIO): The uploaded image file (file-like object).
        lang (str, optional): Language code for OCR. Default is "eng" (English).

    Returns:
        str: Extracted text from the image.
    """
    try:
        # Open image from BytesIO stream
        image = Image.open(io.BytesIO(image_file.read()))
        
        # Extract text using Tesseract OCR
        text = pytesseract.image_to_string(image, lang=lang)
        
        return text.strip()

    except Exception as e:
        return f"Error processing image: {e}"
    
# Extract text from video
def extract_text_from_video(uploaded_video, audio_language='es'):
    try:
        # Save uploaded video to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_video.read())  # Write the uploaded content
            video_path = temp_video.name  # Get the temporary file path

        # Create a temporary WAV file for extracted audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            audio_path = temp_audio.name

        # Extract audio from video using FFmpeg
        ffmpeg.input(video_path).output(audio_path, format="wav").run(overwrite_output=True)

        # Transcribe the extracted audio
        text = extract_text_from_audio(audio_path, audio_language)

        # Clean up temporary files
        os.remove(video_path)
        os.remove(audio_path)

        return text

    except Exception as e:
        return f"Error processing video: {e}"

# Función para generar el prompt del sistema
def create_system_prompt(language):
    prompts = {
        "es": """Eres PsicoChat, un asistente especializado en psicología y salud mental. Tu objetivo es proporcionar apoyo, información y orientación sobre temas de psicología de manera profesional, empática y basada en evidencia científica. Sigue estas pautas:
        1. Sé empático y comprensivo.
        2. Proporciona información basada en evidencia.
        3. Evita diagnósticos o tratamientos específicos.
        4. Recomienda consultar a profesionales cuando sea necesario.
        5. Usa un lenguaje claro y sencillo.
        6. Mantén una postura neutral.
        7. Respeta la confidencialidad.
        8. Ofrece estrategias de afrontamiento.
        9. Reconoce tus límites.
        10. No sustituyas a un profesional.
        Si detectas señales de crisis, ofrece recursos de emergencia.""",
        "en": """You are PsicoChat, an assistant specialized in psychology and mental health. Your goal is to provide support, information, and guidance on psychology topics in a professional, empathetic, and evidence-based manner. Follow these guidelines:
        1. Be empathetic and understanding.
        2. Provide evidence-based information.
        3. Avoid definitive diagnoses or specific treatments.
        4. Recommend consulting professionals when needed.
        5. Use clear and simple language.
        6. Maintain a neutral stance.
        7. Respect confidentiality.
        8. Offer coping strategies.
        9. Acknowledge your limits.
        10. Do not replace a professional.
        If you detect signs of crisis, provide emergency resources.""",
        "fr": """Vous êtes PsicoChat, un assistant spécialisé en psychologie et santé mentale. Votre objectif est de fournir du soutien, des informations et des conseils sur des sujets psychologiques de manière professionnelle, empathique et basée sur des preuves scientifiques. Suivez ces directives :
        1. Soyez empathique et compréhensif.
        2. Fournissez des informations basées sur des preuves.
        3. Évitez les diagnostics définitifs ou les traitements spécifiques.
        4. Recommandez de consulter des professionnels si nécessaire.
        5. Utilisez un langage clair et simple.
        6. Maintenez une posture neutre.
        7. Respectez la confidentialité.
        8. Proposez des stratégies d'adaptation.
        9. Reconnaissez vos limites.
        10. Ne remplacez pas un professionnel.
        En cas de signes de crise, fournissez des ressources d'urgence."""
    }
    return prompts.get(language, prompts["es"])  # Español por defecto

# Función para generar la respuesta con formato específico
def generate_response(prompt, history, pdf_context, mp3_contex, image_context, video_context, language):
    system_prompt = create_system_prompt(language)
    formatted_prompt = f"""<|system|>
    {system_prompt}

    Contexto adicional (de un PDF subido por el usuario):
    {pdf_context}

    Contexto adicional (de un mp3 subido por el usuario):
    {mp3_contex}

    Contexto adicional (de una imagen subida por el usuario):
    {image_context}

    Contexto adicional (de un video subido por el usuario que fue transformado por a texto):
    {video_context}

    <|user|>
    Historial de conversación:
    {history}

    Pregunta actual: {prompt}
    <|assistant|>"""
    return formatted_prompt

# Inicializar el historial del chat y contexto del PDF
if "messages" not in st.session_state:
    st.session_state.messages = []

# Título y descripción
st.title("🧠 PsicoChat - Asistente de Psicología")
st.write("Conversa con un asistente especializado en psicología y salud mental.")

# Sidebar con información y opciones
with st.sidebar:
    st.header("Acerca de PsicoChat")
    st.write("PsicoChat es un asistente virtual diseñado para ofrecer apoyo e información sobre psicología y salud mental.")
    
    # Selector de idioma
    language = st.selectbox("Selecciona el idioma / Select language / Choisissez la langue", ["Español (es)", "English (en)", "Français (fr)"])
    language_code = language.split("(")[1].strip(")")
    
    # Subir PDF para contexto
    uploaded_pdf = st.file_uploader("Sube un PDF para proporcionar contexto adicional", type="pdf")
    if uploaded_pdf:
        pdf_context = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Texto extraído", pdf_context, height=300)
    else:
        pdf_context = ''

    # Subir mp3 para contexto
    uploaded_mp3 = st.file_uploader("Sube un audio en formato mp3 para proporcionar contexto adicional", type=["mp3"])

    if uploaded_mp3:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(uploaded_mp3.read())
            temp_mp3_path = temp_mp3.name

        st.write("Procesando el archivo...")
        mp3_context = extract_text_from_audio(temp_mp3_path, audio_language=language_code)
        st.subheader("Texto extraído:")
        st.write(mp3_context)
        os.remove(temp_mp3_path)
    else:
        mp3_context = ''

    # Subir image para contexto
    uploaded_file = st.file_uploader("Sube una imagen para proporcionar contexto adicional", type=["png", "jpg", "jpeg"])

    if uploaded_file:
        image_context = extract_text_from_image(uploaded_file, lang="spa")  # Spanish OCR
        st.text_area("Extracted Text:", image_context, height=300)
    else:
        image_context = ''

    # Subir video para contexto
    uploaded_video = st.file_uploader("Sube un video para proporcionar contexto adicional", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_video:
        st.video(uploaded_video)  # Display video player

        # Extract text
        with st.spinner("Extracting text..."):
            video_context = extract_text_from_video(uploaded_video, audio_language=language_code)  # Spanish

        # Display the extracted text
        st.text_area("Transcribed Text:", video_context, height=300)
    else:
        video_context = ''
    
    st.header("Recursos de ayuda")
    st.write("""
    - Línea de Prevención del Suicidio (ES): 988
    - Suicide Prevention Lifeline (EN): 988
    - Ligne de prévention du suicide (FR): 01 45 39 40 00
    - Crisis Text Line: Envía HOME al 741741
    - [Psychology Today](https://www.psychologytoday.com)
    """)

# Área principal de chat
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Entrada del usuario
prompt = st.chat_input("Escribe tu pregunta aquí / Write your question here / Écrivez votre question ici...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Preparar el historial completo (sin límite de 5 mensajes)
    history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    
    # Crear el prompt completo con contexto del PDF
    full_prompt = generate_response(prompt,
                                    history,
                                    pdf_context,
                                    mp3_context,
                                    image_context,
                                    video_context,
                                    language_code)
    
    # Obtener respuesta del modelo
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Elaborando respuesta..."):
            try:
                response = client.text_generation(
                    full_prompt,
                    max_new_tokens=1000,  # Aumentado para respuestas más largas
                    stream=True,
                    temperature=0.7,
                    repetition_penalty=1.2
                )
                for chunk in response:
                    full_response = full_response + '' + chunk
                full_response_translated = translate_text(full_response, target_lang=language_code)
                message_placeholder.markdown(full_response_translated)
                #time.sleep(0.01)
            except Exception as e:
                st.error(f"Error: {str(e)}")
                full_response = "Lo siento, hubo un problema. Intenta de nuevo."
                message_placeholder.markdown(full_response)
        
        # Agregar advertencia en caso de crisis
        if any(word in prompt.lower() for word in ["crisis", "suicid", "autolesion", "suicide", "self-harm"]):
            st.markdown("""
            <div class="disclaimer">
            ⚠️ <strong>Importante:</strong> Si estás en crisis o tienes pensamientos suicidas, busca ayuda profesional inmediata.
            </div>
            """, unsafe_allow_html=True)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})

st.markdown("</div>", unsafe_allow_html=True)

# Pie de página
st.markdown("""
<div class="disclaimer">
PsicoChat es una herramienta informativa y no sustituye la atención profesional.
</div>
""", unsafe_allow_html=True)
