let mediaRecorder;
let audioChunks = [];

// Get DOM elements
const startRecordButton = document.getElementById('startRecord');
const stopRecordButton = document.getElementById('stopRecord');
const recordingStatus = document.getElementById('recordingStatus');
const transcriptionResult = document.getElementById('transcription-result');

// Handle file upload form submission
document.getElementById('transcription-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const file = document.getElementById('audio-file').files[0];
    if (file) {
        const formData = new FormData();
        formData.append('audio', file);
        try {
            const response = await fetch('/api/transcribe', {
                method: 'POST',
                body: formData
            });
            const data = await response.json();
            transcriptionResult.textContent = data.transcription;
        } catch (error) {
            console.error('Error:', error);
            transcriptionResult.textContent = 'Error transcribing audio';
        }
    }
});

// Microphone recording functionality
startRecordButton.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream, {
            mimeType: 'audio/webm'
        });
        
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async () => {
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.webm');

            try {
                recordingStatus.textContent = 'Transcribing...';
                const response = await fetch('/api/transcribe', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();
                transcriptionResult.textContent = data.transcription;
                recordingStatus.textContent = '';
            } catch (error) {
                console.error('Error:', error);
                transcriptionResult.textContent = 'Error transcribing audio';
                recordingStatus.textContent = '';
            }

            audioChunks = [];
        };

        mediaRecorder.start();
        startRecordButton.disabled = true;
        stopRecordButton.disabled = false;
        recordingStatus.textContent = 'Recording...';

    } catch (error) {
        console.error('Error accessing microphone:', error);
        recordingStatus.textContent = 'Error accessing microphone';
    }
});

stopRecordButton.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
        startRecordButton.disabled = false;
        stopRecordButton.disabled = true;
        recordingStatus.textContent = 'Processing...';
        
        // Stop all tracks on the stream
        mediaRecorder.stream.getTracks().forEach(track => track.stop());
    }
}); 