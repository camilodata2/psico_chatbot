# Chatbot de Psicología Multimodal

Este proyecto implementa un **chatbot de psicología multimodal** capaz de recibir entradas en múltiples formatos (texto, imagen y audio) y generar respuestas precisas y coherentes en español e inglés. La aplicación está construida sobre:

✅ **Modelos open source de Hugging Face**
✅ **LangChain** para estructurar la conversación
✅ **ChromaDB** para la recuperación de contexto
✅ **Ollama** para la generación de respuestas robustas
✅ **Streamlit** para la interfaz gráfica de usuario
✅ **Sistema de logging** para rastrear las interacciones y errores

---

## 📑 Tabla de Contenidos

- [Características](#características)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalación y Requisitos](#instalación-y-requisitos)
  - [Requisitos del Sistema](#requisitos-del-sistema)
  - [Clonar el Repositorio](#clonar-el-repositorio)
  - [Crear y Activar el Entorno Virtual](#crear-y-activar-el-entorno-virtual)
  - [Instalar las Dependencias](#instalar-las-dependencias)
  - [Configurar Ollama](#configurar-ollama)
  - [Configuración de API Keys (Opcional)](#configuración-de-api-keys-opcional)
- [Configuración](#configuración)
- [Módulos y Funcionalidades](#módulos-y-funcionalidades)
- [Ejecución de la Aplicación](#ejecución-de-la-aplicación)
- [Uso de Ollama](#uso-de-ollama)
- [Registro de Interacciones](#registro-de-interacciones)
- [Notas Adicionales](#notas-adicionales)

---

## 🌟 Características

- **Entrada Multimodal:**Recibe texto, imágenes y audio para generar respuestas precisas.
- **Traducción y Detección de Idioma:**Detecta automáticamente el idioma y traduce las respuestas según sea necesario.
- **Contexto y Memoria:**Utiliza **ChromaDB** para almacenar y recuperar contexto de conversaciones anteriores.
- **Generación de Respuestas con Ollama:**Utiliza un modelo robusto a través de Ollama para generar respuestas contextuales y precisas.
- **Registro y Seguimiento:**
  Cada interacción y error se registra en un archivo de log.

---

## 📂 Estructura del Proyecto

```plaintext
chatbot-psicologia/
├── main.py
├── config.py
├── requirements.txt
├── models/
│   ├── __init__.py
│   ├── audio.py
│   ├── image.py
│   ├── language.py
│   └── conversation.py
└── utils/
    ├── __init__.py
    ├── helpers.py
    └── logger.py
```

Descripción de los archivos:

✅ main.py: Archivo principal que inicia la interfaz gráfica (Streamlit).
✅ config.py: Configuración de modelos
✅ requirements.txt: Lista de dependencias.
✅ models/:

    audio.py – Procesamiento de archivos de audio
    image.py – Procesamiento de imágenes
    language.py – Traducción y detección de idioma
    conversation.py – Generación de respuestas usando Ollama y recuperación de contexto con ChromaDB

✅ utils/:

    logger.py – Registro de eventos y errores
    helpers.py – Funciones auxiliares

🛠️ Instalación y Requisitos
✅ Requisitos del Sistema

    Python ≥ 3.8
    GPU (opcional, para un mejor rendimiento)
    Conexión a Internet (para descargar modelos de Hugging Face)

```
```
```

```
```pip install -U sentence-transformers

```
