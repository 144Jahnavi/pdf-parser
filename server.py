from flask import Flask, request, jsonify

# Ensure extract.py is correctly imported
from extract import extract_text_from_pdf, extract_text_from_image  

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the PDF Parser API!"

# PDF Upload Route
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    text = extract_text_from_pdf(file)
    return jsonify({'extracted_text': text})

# Image Upload Route
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    text = extract_text_from_image(file)
    return jsonify({'extracted_text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
