import os
import tempfile
from . import socketio
import whisper
from flask_socketio import emit
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load Whisper model once
try:
    model = whisper.load_model("base")
    logger.info("Whisper model loaded successfully")
except Exception as e:
    logger.error(f"Error loading Whisper model: {e}")

@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')
    emit('status', {'message': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')

@socketio.on('audio_data')
def handle_audio_data(audio_data):
    logger.info('Received audio data')
    
    try:
        # Create temporary file for the audio chunk
        with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
            temp_file.write(audio_data)
            temp_path = temp_file.name
            logger.debug(f'Saved audio to temporary file: {temp_path}')

        # Transcribe the audio chunk
        result = model.transcribe(temp_path)
        logger.info(f'Transcription result: {result["text"]}')
        
        # Send transcription back to client
        emit('transcription', {'text': result['text']})
    
    except Exception as e:
        logger.error(f'Error processing audio: {e}')
        emit('error', {'message': str(e)})
    
    finally:
        # Clean up temporary file
        try:
            os.unlink(temp_path)
            logger.debug('Temporary file cleaned up')
        except Exception as e:
            logger.error(f'Error cleaning up temporary file: {e}') 