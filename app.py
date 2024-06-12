from flask import Flask, request, jsonify, render_template
from speech_to_text import transcribe_audio_tpu
from phrase_handler import handle_phrase

app = Flask(__name__)

# Directories for videos and alphabet images
VIDEO_DIRECTORY = "Data-Set/Videos"
ALPHABET_DIRECTORY = "Data-Set/Alphabet"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    audio_file = request.files['file']
    transcription = transcribe_audio_tpu(audio_file)
    result = handle_phrase(transcription, VIDEO_DIRECTORY, ALPHABET_DIRECTORY)
    return jsonify({'transcription': transcription, 'result': result})

if __name__ == '__main__':
    app.run(debug=True)
