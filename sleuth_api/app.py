from flask import Flask, request, jsonify, send_file
from flask_httpauth import HTTPBasicAuth
from models import db, bcrypt, User, File
from datetime import datetime
import os
from image_denc import encode_image, decode_image
from audio_denc import encode_audio, decode_audio
from video_denc import encode_video, decode_video
from utils import encrypt_message, decrypt_message


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ENCODED_FOLDER'] = 'encoded'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///files.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
auth = HTTPBasicAuth()

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['ENCODED_FOLDER']):
    os.makedirs(app.config['ENCODED_FOLDER'])

with app.app_context():
    db.create_all()

@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        return user
    return None

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'User already exists'}), 400

    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/encode_image', methods=['POST'])
@auth.login_required
def encode_image_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    message = request.form.get('message', '')
    password = request.form.get('password', '')
    if not message or not password:
        return jsonify({'error': 'Message and password are required'}), 400

    encrypted_message = encrypt_message(message, password)
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    output_filename = f"encoded_{filename}"
    output_path = os.path.join(app.config['ENCODED_FOLDER'], output_filename)
    
    try:
        encode_image(file_path, encrypted_message, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_record = File(filename=filename, encoded_filename=output_filename, upload_date=datetime.utcnow(), message=encrypted_message, user_id=auth.current_user().id)
    db.session.add(file_record)
    db.session.commit()
    
    return send_file(output_path, as_attachment=True, download_name=output_filename)

@app.route('/decode_image', methods=['POST'])
@auth.login_required
def decode_image_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    password = request.form.get('password', '')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        encrypted_message = decode_image(file_path)
        message = decrypt_message(encrypted_message, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': message})

@app.route('/encode_audio', methods=['POST'])
@auth.login_required
def encode_audio_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    message = request.form.get('message', '')
    password = request.form.get('password', '')
    if not message or not password:
        return jsonify({'error': 'Message and password are required'}), 400

    encrypted_message = encrypt_message(message, password)
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    output_filename = f"encoded_{filename}"
    output_path = os.path.join(app.config['ENCODED_FOLDER'], output_filename)
    
    try:
        encode_audio(file_path, encrypted_message, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_record = File(filename=filename, encoded_filename=output_filename, upload_date=datetime.utcnow(), message=encrypted_message, user_id=auth.current_user().id)
    db.session.add(file_record)
    db.session.commit()
    
    return send_file(output_path, as_attachment=True, download_name=output_filename)

@app.route('/decode_audio', methods=['POST'])
@auth.login_required
def decode_audio_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    password = request.form.get('password', '')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        encrypted_message = decode_audio(file_path)
        message = decrypt_message(encrypted_message, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': message})

@app.route('/encode_video', methods=['POST'])
@auth.login_required
def encode_video_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    message = request.form.get('message', '')
    password = request.form.get('password', '')
    if not message or not password:
        return jsonify({'error': 'Message and password are required'}), 400

    encrypted_message = encrypt_message(message, password)
    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    output_filename = f"encoded_{filename}"
    output_path = os.path.join(app.config['ENCODED_FOLDER'], output_filename)
    
    try:
        encode_video(file_path, encrypted_message, output_path)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    file_record = File(filename=filename, encoded_filename=output_filename, upload_date=datetime.utcnow(), message=encrypted_message, user_id=auth.current_user().id)
    db.session.add(file_record)
    db.session.commit()
    
    return send_file(output_path, as_attachment=True, download_name=output_filename)

@app.route('/decode_video', methods=['POST'])
@auth.login_required
def decode_video_route():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    password = request.form.get('password', '')
    if not password:
        return jsonify({'error': 'Password is required'}), 400

    filename = file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    try:
        encrypted_message = decode_video(file_path)
        message = decrypt_message(encrypted_message, password)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'message': message})


@app.route('/')
def index():
    return "Welcome to Sleuth API"


if __name__ == '__main__':
    app.run(debug=True)
