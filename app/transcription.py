import speech_recognition as sr
from pydub import AudioSegment
import os

def transcribe_audio(file_path):
    # Convert webm to wav
    audio = AudioSegment.from_file(file_path)
    wav_path = file_path.rsplit('.', 1)[0] + '.wav'
    audio.export(wav_path, format="wav")

    # Initialize recognizer
    r = sr.Recognizer()
    
    # Transcribe
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
        try:
            text = r.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Could not request results; {e}"
        finally:
            # Clean up temporary files
            os.remove(wav_path)
            if os.path.exists(file_path):
                os.remove(file_path)