import streamlit as st
from modules.text_extraction import extract_text_from_pdf, extract_text_from_audio, extract_text_from_image, extract_text_from_video
from modules.translation import translate_text
from modules.chat_logic import generate_response
from modules.settings import client

# Configurar la aplicación
st.set_page_config(page_title="PsicoChat - Asistente de Psicología", page_icon="🧠", layout="wide")

st.title("🧠 PsicoChat - Asistente de Psicología")
st.write("Conversa con un asistente especializado en psicología y salud mental.")

# Sidebar con opciones
with st.sidebar:
    st.header("Acerca de PsicoChat")
    language = st.selectbox("Selecciona el idioma", ["Español (es)", "English (en)", "Français (fr)"])
    language_code = language.split("(")[1].strip(")")

    uploaded_pdf = st.file_uploader("Sube un PDF", type=["pdf"])
    uploaded_audio = st.file_uploader("Sube un archivo de audio", type=["mp3", "wav"])
    uploaded_image = st.file_uploader("Sube una imagen", type=["png", "jpg", "jpeg"])
    uploaded_video = st.file_uploader("Sube un video", type=["mp4"])

# Procesamiento de archivos
pdf_context = extract_text_from_pdf(uploaded_pdf) if uploaded_pdf else ""
audio_context = extract_text_from_audio(uploaded_audio) if uploaded_audio else ""
image_context = extract_text_from_image(uploaded_image) if uploaded_image else ""
video_context = extract_text_from_video(uploaded_video) if uploaded_video else ""

# Inicializar historial del chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Entrada de usuario
user_input = st.text_input("Escribe tu mensaje aquí...")

if st.button("Enviar") and user_input:
    history = "\n".join(st.session_state.messages)
    formatted_prompt = generate_response(user_input, history, pdf_context, audio_context, image_context, video_context, language_code)
    
    response = client.text_generation(formatted_prompt)
    
    st.session_state.messages.append(f"👤 Usuario: {user_input}")
    st.session_state.messages.append(f"🤖 PsicoChat: {response}")

    for msg in st.session_state.messages:
        st.write(msg)
