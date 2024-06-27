
from flask import Flask, request, jsonify, send_file
import os
from image_denc import encode_image, decode_image
from models import db, File
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCODED_FOLDER'] = 'encoded'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['ENCODED_FOLDER']):
    os.makedirs(app.config['ENCODED_FOLDER'])

with app.app_context():
    db.create_all()

@app.route('/encode', methods=['POST'])
def encode():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    message = request.form.get('message', '')
    if not message:
        return jsonify({'error': 'No message provided'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    output_filename = f"encoded_{filename}"
    output_path = os.path.join(app.config['ENCODED_FOLDER'], output_filename)
    
    try:
        encode_image(file_path, message, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_record = File(filename=filename, encoded_filename=output_filename, upload_date=datetime.utcnow(), message=message)
    db.session.add(file_record)
    db.session.commit()
    
    return send_file(output_path, as_attachment=True, mimetype='application/octet-stream', download_name=output_filename)


@app.route('/decode', methods=['POST'])
def decode():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        message = decode_image(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': message})

@app.route('/')
def index():
    return "Image Steganography API"

if __name__ == '__main__':
    app.run(debug=True)
