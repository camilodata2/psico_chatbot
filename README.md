# PsicoChat: Asistente de Psicología basado en IA

## 📋 Descripción

PsicoChat es un chatbot de asistencia psicológica que utiliza inteligencia artificial generativa para proporcionar apoyo emocional, información sobre salud mental y estrategias de afrontamiento básicas a usuarios en diferentes idiomas, con capacidad para procesar y contextualizar información de diferentes formatos multimedia.

## 🔍 Problema

La salud mental es una preocupación prioritaria a nivel global. Según la OMS, más de 264 millones de personas sufren de depresión, y aproximadamente 800,000 personas mueren por suicidio cada año. El acceso a recursos de salud mental sigue siendo limitado debido a:

- Escasez de profesionales
- Barreras económicas
- Estigma social
- Barreras geográficas
- Limitaciones de tiempo

PsicoChat busca crear una herramienta accesible que proporcione un primer nivel de apoyo psicológico y orientación, complementando la atención profesional.

## ✅ Objetivos

- Proporcionar un sistema de conversación natural basado en modelos de lenguaje
- Desarrollar capacidades multimodales (texto, audio, imágenes y video)
- Ofrecer soporte en múltiples idiomas (español, inglés y francés)
- Crear una interfaz intuitiva y accesible
- Diseñar un sistema que reconozca situaciones de crisis

## ⚠️ Limitaciones

- No sustituye la atención profesional de salud mental
- No puede realizar diagnósticos clínicos
- No está diseñado para intervenir en crisis agudas
- La precisión del procesamiento multimedia depende de la calidad de los archivos

## 👥 Usuarios Objetivo

- Población general interesada en información sobre salud mental
- Personas que experimentan dificultades emocionales leves a moderadas
- Usuarios con barreras de acceso a servicios de salud mental convencionales
- Profesionales de la salud como herramienta complementaria

## 🔧 Arquitectura Técnica

PsicoChat está diseñado como una aplicación web basada en Streamlit con la siguiente arquitectura:

- **Interfaz de Usuario**: Desarrollada con Streamlit
- **Procesamiento de Lenguaje Natural**: Basado en el modelo "mistralai/Mistral-7B-Instruct-v0.2" de Hugging Face
- **Procesamiento Multimedia**:
  - PDF: PyPDF2
  - Imágenes: Tesseract OCR
  - Audio: Speech Recognition y Pydub
  - Video: FFmpeg y Speech Recognition
- **Traducción**: langdetect y googletrans

## 🔄 Flujo de Trabajo

1. El usuario accede a la interfaz web
2. Selecciona el idioma y opcionalmente carga archivos multimedia
3. Introduce preguntas o comentarios
4. El sistema procesa la entrada y genera respuestas contextualizadas
5. Si es necesario, se activan protocolos de detección de crisis

## 📊 Desempeño



## 🔒 Privacidad y Seguridad

- No almacenamiento permanente de conversaciones o archivos
- Procesamiento local cuando es posible
- No se solicitan datos personales
- Información clara sobre alcance y limitaciones


## ⚖️ Consideraciones Éticas

PsicoChat se ha desarrollado con un fuerte compromiso hacia la ética, respetando la privacidad del usuario y estableciendo límites claros sobre sus capacidades y alcance como herramienta complementaria, nunca sustitutiva, de la atención profesional.
