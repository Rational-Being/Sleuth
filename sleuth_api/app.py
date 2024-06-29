
from flask import Flask, request, jsonify, send_file
import os
from image_denc import encode_image, decode_image
from models import db, File
from datetime import datetime
from audio_denc import decode_audio, encode_audio
from video_denc import encode_video, decode_video


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


@app.route('/encode_audio', methods=['POST'])
def encode_audio_route():
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
        encode_audio(file_path, message, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_record = File(filename=filename, encoded_filename=output_filename, upload_date=datetime.utcnow(), message=message)
    db.session.add(file_record)
    db.session.commit()
    
    return send_file(output_path, as_attachment=True, download_name=output_filename)

@app.route('/decode_audio', methods=['POST'])
def decode_audio_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        message = decode_audio(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': message})

@app.route('/encode_video', methods=['POST'])
def encode_video_route():
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
        encode_video(file_path, message, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_record = File(filename=filename, encoded_filename=output_filename, upload_date=datetime.utcnow(), message=message)
    db.session.add(file_record)
    db.session.commit()
    
    return send_file(output_path, as_attachment=True, download_name=output_filename)

@app.route('/decode_video', methods=['POST'])
def decode_video_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        message = decode_video(file_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': message})

import cv2
import numpy as np

def encode_video(video_path, message, output_path):
    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(output_path, fourcc, 20.0, (int(cap.get(3)), int(cap.get(4))))

    message += chr(0)  # Null-terminate the message
    bin_message = ''.join(format(ord(char), '08b') for char in message)
    message_len = len(bin_message)
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx < message_len:
            frame_flat = frame.flatten()
            for i in range(0, 3 * (frame.shape[0] * frame.shape[1]), 3):
                if frame_idx < message_len:
                    frame_flat[i] = (frame_flat[i] & ~1) | int(bin_message[frame_idx])
                    frame_idx += 1
                else:
                    break
            frame = frame_flat.reshape(frame.shape)

        out.write(frame)

    cap.release()
    out.release()

def decode_video(video_path):
    cap = cv2.VideoCapture(video_path)
    bin_message = ''
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_flat = frame.flatten()
        for i in range(0, 3 * (frame.shape[0] * frame.shape[1]), 3):
            bin_message += str(frame_flat[i] & 1)

    cap.release()

    message = ''.join(chr(int(bin_message[i:i+8], 2)) for i in range(0, len(bin_message), 8))
    return message.split(chr(0))[0]  # Stop at the null character



@app.route('/')
def index():
    return "Welcome to Sleuth"

if __name__ == '__main__':
    app.run(debug=True)
