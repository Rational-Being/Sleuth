from PIL import Image


# encode_image: Encodes a steganographic message into an image file.
# decode_image: Decodes a steganographic image and extracts the hidden message.
def encode_image(image_path, message, output_path):
    """
    Encodes a steganographic message into an image file.

    Parameters:
    image_path (str): The path to the original image file.
    message (str): The message to be hidden within the image.
    output_path (str): The path where the encoded image will be saved.

    Raises:
    FileNotFoundError: If the specified image file does not exist.
    IOError: If there is an issue opening the image file.
    """
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    message += chr(0)  # Null-terminate the message
    bin_message = "".join(format(ord(char), "08b") for char in message)
    idx = 0

    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            for n in range(3):
                if idx < len(bin_message):
                    pixel[n] = int(format(pixel[n], "08b")[:-1] + bin_message[idx], 2)
                    idx += 1
            encoded.putpixel((x, y), tuple(pixel))

    encoded.save(output_path)


def decode_image(image_path):
    """
    Decodes a steganographic image and extracts the hidden message.

    Parameters:
    image_path (str): The path to the steganographic image file.

    Returns:
    str: The extracted hidden message. If an error occurs during decoding, returns None.

    Raises:
    FileNotFoundError: If the specified image file does not exist.
    IOError: If there is an issue opening the image file.
    """
    try:
        image = Image.open(image_path)
    except FileNotFoundError:
        print(f"Error: File not found - {image_path}")
        return None
    except IOError:
        print(f"Error: Unable to open image - {image_path}")
        return None

    bin_message = ""
    width, height = image.size

    # Iterate through each pixel in the image
    for y in range(height):
        for x in range(width):
            pixel = list(image.getpixel((x, y)))
            # Extract the least significant bit from each color channel
            for n in range(3):
                bin_message += format(pixel[n], "08b")[-1]

    # Convert binary message to string
    message = "".join(
        chr(int(bin_message[i : i + 8], 2)) for i in range(0, len(bin_message), 8)
    )
    # Stop at the null character
    return message.split(chr(0))[0]
