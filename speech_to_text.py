# speech_to_text.py
import whisper
import tempfile
import os

# Load model once at startup to avoid reloading for each request
model = whisper.load_model("small")

def convert_speech_to_text(audio_file):
    """
    Takes an uploaded audio file (like .webm), transcribes it using Whisper,
    and returns the transcribed text.
    """
    try:
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
            audio_file.save(tmp.name)
            temp_path = tmp.name

        # Run Whisper transcription
        result = model.transcribe(temp_path)

        # Clean up temp file
        os.remove(temp_path)

        return result.get("text", "").strip()

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
