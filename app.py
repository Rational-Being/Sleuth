from flask import Flask, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename  # to sanitize the filename
from image_denc import encode_image, decode_image
from flask.helpers import send_file, send_from_directory

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["ENCODED_FOLDER"] = "encoded"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB max file size
app.config["ALLOWED_EXTENSIONS"] = {"png", "jpg", "jpeg"}

if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

if not os.path.exists(app.config["ENCODED_FOLDER"]):
    os.makedirs(app.config["ENCODED_FOLDER"])


# sanitize file name to avoid upload of malicous files like php backdoor
def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
    )


@app.route("/encode", methods=["POST"])
def encode():
    """
    Encodes a message into a steganographic image.

    This function handles POST requests to the '/encode' endpoint. It expects a file
    and a message in the request body. The file should be an image file, and the message
    should be a string of text.

    The function performs the following steps:
    1. Validates the request to ensure that a file and a message are provided.
    2. Sanitizes the file name to avoid potential security issues.
    3. Checks the file type to ensure that it is an allowed extension.
    4. Checks the message length to ensure that it is within an acceptable range.
    5. Saves the file to the server.
    6. Encodes the message into the image using the 'encode_image' function.
    7. Returns the encoded image as a downloadable file.

    Returns:
    JSON response with a success message or an error message.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type"}), 400

    message = request.form.get("message", "")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    if len(message) > 1024:  # arbitrary max message length
        return jsonify({"error": "Message too long"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    try:
        file.save(file_path)
    except Exception as e:
        return jsonify({"error": "Error saving file: " + str(e)}), 500

    output_filename = f"encoded_{filename}"
    output_path = os.path.join(app.config["ENCODED_FOLDER"], output_filename)

    try:
        encode_image(file_path, message, output_path)
    except Exception as e:
        return jsonify({"error": "Error encoding image: " + str(e)}), 500

    return send_from_directory(
        app.config["ENCODED_FOLDER"], output_filename, as_attachment=True
    )
@app.route("/decode", methods=["POST"])
def decode():
    """
    Decodes a steganographic image and extracts the hidden message.

    This route handles POST requests to the '/decode' endpoint. It expects a file
    in the request body. The file should be a steganographic image encoded with
    the 'encode_image' function.

    If the request is valid and the file is successfully decoded, the function
    returns a JSON response with the decoded message. If there is an error during
    the decoding process, the function returns a JSON response with an error message.

    Returns:
    JSON response with the decoded message or an error message.
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    print("Received file:", file)
    print("File filename:", file.filename)

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    file.save(file_path)

    print("File saved to:", file_path)

    try:
        message = decode_image(file_path)
        print("Decoded message:", message)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"message": message})


@app.route("/")
def index():
    return "Image Steganography API"


if __name__ == "__main__":
    app.run(debug=True)  # disable debug mode in production
