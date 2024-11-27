from app.transcription import transcribe_audio
import os

def test_transcription():
    # 1. Create a test audio file path (replace with your actual test file)
    test_file = "test_files/harvard 2.wav"  # Make sure this file exists
    
    # 2. Print file existence check
    print(f"File exists before transcription: {os.path.exists(test_file)}")
    
    # 3. Try transcription with detailed error handling
    try:
        result = transcribe_audio(test_file)
        print(f"Transcription result: {result}")
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    test_transcription() 