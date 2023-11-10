from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS  # Enables cross-origin resource sharing
from interaction.interaction_handler import InteractionHandler
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains on all routes
app.config['UPLOAD_FOLDER'] = 'uploads'  # Configure a folder to save uploaded files

interaction_handler = InteractionHandler()

@app.route('/interact', methods=['POST'])
def interact():
    # Ensure request is in JSON format
    if not request.is_json:
        return jsonify({"error": "Invalid input, JSON expected"}), 400

    # Extract user input from request
    user_input = request.json.get('input')

    # Validate user input is string and non-empty
    if not isinstance(user_input, str) or not user_input.strip():
        return jsonify({"error": "Input text cannot be empty"}), 400

    response_data = interaction_handler.handle_user_input(user_input)
    return jsonify(response_data)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        # Evaluate if any processing is needed based on file_type and handle accordingly
        return jsonify({"success": "File successfully uploaded", "file_path": file_path}), 201

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    # Security check - full path should never be exposed & directory transversal should be handled
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Other routes and the previous Flask app logic remain unchanged...

if __name__ == '__main__':
    app.run(debug=True)
