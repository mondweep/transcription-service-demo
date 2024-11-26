from flask import Blueprint, jsonify, request, render_template
from .transcription import transcribe_audio

# Create the blueprint
bp = Blueprint('api', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/api/transcribe', methods=['POST'])
def transcribe():
    file = request.files['audio']
    file_path = f'/tmp/{file.filename}'
    file.save(file_path)
    transcription = transcribe_audio(file_path)
    return jsonify({'transcription': transcription}) 