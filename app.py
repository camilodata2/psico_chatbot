import os
import io
import tempfile
import streamlit as st
from modules.text_extraction import extract_text_from_pdf, extract_text_from_audio, extract_text_from_image, extract_text_from_video
from modules.translation import translate_text
from modules.chat_logic import generate_response
from modules.settings import client

# Configurar la aplicación
st.set_page_config(page_title="PsicoChat - Asistente de Psicología", page_icon="🧠", layout="wide")

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

st.title("🧠 PsicoChat - Asistente de Psicología")
st.write("Conversa con un asistente especializado en psicología y salud mental.")

# Sidebar con opciones
with st.sidebar:
    st.header("Acerca de PsicoChat")
    st.write("PsicoChat es un asistente virtual diseñado para ofrecer apoyo e información sobre psicología y salud mental.")
    
    language = st.selectbox("Selecciona el idioma / Select language / Choisissez la langue", ["Español (es)", "English (en)", "Français (fr)"])
    language_code = language.split("(")[1].strip(")")

    uploaded_pdf = st.file_uploader("Sube un PDF", type=["pdf"])
    if uploaded_pdf:
        pdf_context = extract_text_from_pdf(uploaded_pdf)
        st.text_area("Texto extraído", pdf_context, height=300)
    else:
        pdf_context = ''

    uploaded_audio = st.file_uploader("Sube un archivo de audio", type=["mp3", "wav"])
    if uploaded_audio:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_mp3:
            temp_mp3.write(uploaded_audio.read())
            temp_mp3_path = temp_mp3.name

        st.write("Procesando el archivo...")
        print(language_code)
        audio_context = extract_text_from_audio(temp_mp3_path, language=language_code)
        st.subheader("Texto extraído:")
        st.write(audio_context)
        os.remove(temp_mp3_path)
    else:
        audio_context = ''
    
    uploaded_image = st.file_uploader("Sube una imagen para proporcionar contexto adicional", type=["png", "jpg", "jpeg"])
    if uploaded_image:
        image_context = extract_text_from_image(uploaded_image, lang="spa")  # Spanish OCR
        st.text_area("Extracted Text:", image_context, height=300)
    else:
        image_context = ''

    uploaded_video = st.file_uploader("Sube un video para proporcionar contexto adicional", type=["mp4", "mov", "avi", "mkv"])

    if uploaded_video:
        st.video(uploaded_video)

        with st.spinner("Extracting text..."):
            video_context = extract_text_from_video(uploaded_video, audio_language=language_code)  # Spanish

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

# Inicializa el chat
if "messages" not in st.session_state:
    print('Messages list is empty')
    st.session_state.messages = []

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
# Entrada del usuario
prompt = st.chat_input("Escribe tu pregunta aquí / Write your question here / Écrivez votre question ici...")

if prompt:
    st.session_state.messages.append({"role": "Usuario", "content": prompt})
    with st.chat_message("Usuario"):
        st.markdown(prompt)

    # Preparar el historial completo (sin límite de 5 mensajes)
    history = "\n".join([f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.messages])
    
    # Crear el prompt completo con contexto del PDF
    full_prompt = generate_response(prompt,
                                    history,
                                    pdf_context,
                                    audio_context,
                                    image_context,
                                    video_context,
                                    language_code)
    print(full_prompt)
    # Obtener respuesta del modelo
    with st.chat_message("PsicoChat"):
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
                print(type(response))
                for chunk in response:
                    full_response += chunk
                #full_response_translated = translate_text(full_response, target_lang=language_code)
                    message_placeholder.markdown(full_response)
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
    
    st.session_state.messages.append({"role": "🤖 PsicoChat", "content": full_response})

st.markdown("</div>", unsafe_allow_html=True)

# Pie de página
st.markdown("""
<div class="disclaimer">
PsicoChat es una herramienta informativa y no sustituye la atención profesional.
</div>
""", unsafe_allow_html=True)
