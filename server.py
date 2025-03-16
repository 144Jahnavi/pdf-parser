from flask import Flask, request, jsonify
from extract import extract_text_from_pdf, extract_text_from_image  # Ensure this module exists

app = Flask(__name__)

# Define a test route
@app.route('/')
def home():
    return "Welcome to the PDF Parser API!"

# Define an API endpoint to upload a PDF
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    text = extract_text_from_pdf(file)
    return jsonify({'extracted_text': text})

# Define an API endpoint to upload an Image
@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    text = extract_text_from_image(file)
    return jsonify({'extracted_text': text})

if __name__ == '__main__':
    app.run(debug=True)
