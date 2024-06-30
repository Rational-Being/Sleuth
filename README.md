#  Sleuth
## Steganography Web Application

This project is a web application that allows users to encode and decode hidden messages within multimedia files (images, audio, and video). The backend is built using Flask. The application supports user authentication and encrypts hidden messages to enhance security.

## Features

- **User Authentication**: Secure login and registration functionality to restrict access to the encoding and decoding API.
- **Image Steganography**: Encode and decode messages within image files.
- **Audio Steganography**: Encode and decode messages within audio files.
- **Video Steganography**: Encode and decode messages within video files.
- **Message Encryption**: Encrypt messages before encoding them to enhance security.
- **Database Integration**: Store user information and uploaded files using SQLite.

## Technologies Used

### Backend

- Flask
- SQLAlchemy
- Flask-HTTPAuth
- PyCryptodome
- Flask-Bcrypt

### Multimedia Processing

- OpenCV (for image processing)
- Pydub (for audio processing)
- FFmpeg/PyAV (for video processing)

## Installation

### Prerequisites

- Python 3.8 or higher

### Backend Setup

1. **Clone the repository and install the dependencies**:
    ```sh
    git clone https://github.com/Rational-Being/Sleuth.git
    pip install -r requirements.txt
    cd sleuth_api
    ```

2. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Run the Flask application**:
    ```sh
    export FLASK_APP=app.py
    flask run
    ```
The application will now be running on `http://localhost:5000`

## Usage

### Register a New User

Send a POST request to `/register` with the following JSON payload:

```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### Encoding a Message

1. **Image Encoding**:
    - Endpoint: `/encode_image`
    - Method: POST
    - Authentication: Basic Auth (username and password)
    - Form Data:
        - `file`: The image file
        - `message`: The message to encode
        - `password`: The password to encrypt the message

2. **Audio Encoding**:
    - Endpoint: `/encode_audio`
    - Method: POST
    - Authentication: Basic Auth (username and password)
    - Form Data:
        - `file`: The audio file
        - `message`: The message to encode
        - `password`: The password to encrypt the message

3. **Video Encoding**:
    - Endpoint: `/encode_video`
    - Method: POST
    - Authentication: Basic Auth (username and password)
    - Form Data:
        - `file`: The video file
        - `message`: The message to encode
        - `password`: The password to encrypt the message

### Decoding a Message

1. **Image Decoding**:
    - Endpoint: `/decode_image`
    - Method: POST
    - Authentication: Basic Auth (username and password)
    - Form Data:
        - `file`: The encoded image file
        - `password`: The password used to encrypt the message

2. **Audio Decoding**:
    - Endpoint: `/decode_audio`
    - Method: POST
    - Authentication: Basic Auth (username and password)
    - Form Data:
        - `file`: The encoded audio file
        - `password`: The password used to encrypt the message

3. **Video Decoding**:
    - Endpoint: `/decode_video`
    - Method: POST
    - Authentication: Basic Auth (username and password)
    - Form Data:
        - `file`: The encoded video file
        - `password`: The password used to encrypt the message

### Example cURL Commands

**Encode an Image**:
```sh
curl -u username:password -X POST -F "file=@path_to_your_image.png" -F "message=Your secret message" -F "password=strong_password" http://127.0.0.1:5000/encode_image --output encoded_image.png
```

**Decode an Image**:
```sh
curl -u username:password -X POST -F "file=@encoded_image.png" -F "password=strong_password" http://127.0.0.1:5000/decode_image
```

## Project Structure

```
Sleuth
├── sleuth_api/
│   ├── app.py
│   ├── models.py
│   ├── utils.py
│   ├── image_denc.py
│   ├── audio_denc.py
│   ├── video_denc.py
│   ├── uploads/
│   ├── encoded/
└── docs/
    ├── audio encode and decode
    ├── image encode and decode
    ├── user authentication
    ├── video encode and decode
├── README.md 
├── sleuth.png (sample image files)
├── sleuth-3s.wav (sample audio file)
├── sleauth.avi (sample video file)
├── requirements.txt
```

## Stegnography types
 LSB stegnography (used in this project)
 Transform domain steganography
 Steganlyis, Deep Stegnogrpahy
 Spread-Spectrum Stegnography