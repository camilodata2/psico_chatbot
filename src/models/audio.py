import os
import whisper
import sys
import numpy as np
import tempfile


def transcribe_audio(audio_file):
    """
    Transcribe the content of an audio file to text using the Whisper model.
    """
    try:
        print('I enter the model to read the audio')
        print(type(audio_file))

        if not audio_file:
            print("No file provided.")
            return None

        # Save the UploadedFile as a temporary file
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            temp_audio.write(audio_file.read())  # Write file content
            temp_audio.flush()  # Ensure data is written
            
            model = whisper.load_model("small")
            print("I've read the audio")

            # Transcribe the audio from the saved file
            result = model.transcribe(temp_audio.name)

        print(result)
        return result["text"]

    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None
    
if __name__ == "__main__":
    temp_file_path = "/mnt/c/Users/Estiben/OneDrive/Escritorio/psico_chatbot/input/audio.mp3"

    if not os.path.isfile(temp_file_path):
        print(f"File not found: {temp_file_path}")
        sys.exit(1)

    transcription = transcribe_audio(temp_file_path)
    if transcription:
        print("Transcription:")
        print(transcription)
