# speech_to_text.py
import whisper
import tempfile
import os
import subprocess

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
            webm_path = tmp.name
            wav_path = webm_path.replace(".webm", ".wav")

        # Convert webm -> wav (16kHz mono)
        subprocess.run([
            "ffmpeg", "-i", webm_path,
            "-ar", "16000", "-ac", "1", wav_path
        ], check=True)

        # Transcribe with Whisper
        result = model.transcribe(wav_path)

        # Cleanup
        os.remove(webm_path)
        os.remove(wav_path)

        return result.get("text", "").strip()

    except Exception as e:
        print(f"Error during transcription: {e}")
        return None
