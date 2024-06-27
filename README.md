Sleuth is a steganography tool designed to securely embed and extract hidden information within various digital media formats, such as images, audio, and video. The tool provides advanced features such as encryption, customizable algorithms, data integrity checks, and steganalysis capabilities, all within a user-friendly interface and a powerful command-line option.


## image_denc.py

The `image_denc.py` file contains two functions for encoding and decoding steganographic messages within image files.

### encode_image

The `encode_image` function encodes a steganographic message into an image file. It takes three parameters:

- `image_path` (str): The path to the original image file.
- `message` (str): The message to be hidden within the image.
- `output_path` (str): The path where the encoded image will be saved.

The function uses the Python Imaging Library (PIL) to open the original image, create a copy of the image, and iterate through each pixel to hide the message. The message is converted to binary format and stored in the least significant bits of the color channels.

### decode_image

The `decode_image` function decodes a steganographic image and extracts the hidden message. It takes one parameter:

- `image_path` (str): The path to the steganographic image file.

The function uses the PIL to open the image and iterate through each pixel to extract the hidden message. The binary message is converted back to a string format.

The `decode_image` function returns the extracted hidden message as a string. If an error occurs during decoding, it returns `None`.

You can use these functions in your Flask application to handle the encoding and decoding of steganographic images.
