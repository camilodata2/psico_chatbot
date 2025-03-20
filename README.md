# 📌 Requisitos del Sistema

## 🖥️ Requisitos del Entorno

- **Sistema Operativo:** Windows, macOS o Linux.
- **Python:** Versión **3.8 o superior**.
- **Entorno virtual (opcional pero recomendado):** `venv` o `conda`.

## 📦 Instalación de Dependencias

Ejecuta el siguiente comando para instalar todas las dependencias necesarias:

```bash
pip install -r requirements.txt
```

### **Archivo `requirements.txt`**

```txt
streamlit
python-dotenv
huggingface_hub
pytesseract
PyPDF2
speechrecognition
pydub
langdetect
googletrans==4.0.0-rc1
Pillow
ffmpeg-python
```

### 🔧 **Instalación de `ffmpeg` (Requerido para procesamiento de audio y video)**

- **Windows:** Descargar desde [FFmpeg Official](https://ffmpeg.org/download.html) e instalar.
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update && sudo apt install ffmpeg
  ```
- **macOS (Homebrew):**
  ```bash
  brew install ffmpeg
  ```

## 🔑 Configuración de Variables de Entorno

Crea un archivo **`.env`** en el directorio del proyecto con el siguiente contenido:

```txt
HUGGINGFACE_API_KEY=TU_CLAVE_DE_HUGGINGFACE
```

Puedes obtener una API Key en [Hugging Face](https://huggingface.co/settings/tokens).

## 🖼️ Instalación de Tesseract OCR (Para extracción de texto en imágenes)

- **Windows:** Descargar desde [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) e instalar. Luego, agregar la ruta en el código:
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```
- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt install tesseract-ocr
  ```
- **macOS:**
  ```bash
  brew install tesseract
  ```

## 🚀 Ejecución del Proyecto

1. **Activar el entorno virtual** (si usas uno):
   ```bash
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
2. **Ejecutar la aplicación con Streamlit:**
   ```bash
   streamlit run nombre_del_archivo.py
   ```

Con estos pasos, el sistema estará listo para ejecutarse correctamente. 🎯
