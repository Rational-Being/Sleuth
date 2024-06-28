from pydub import AudioSegment
import numpy as np

def encode_audio(audio_path, message, output_path):
    """
    This function encodes a given message into an audio file using LSB steganography.

    Parameters:
    audio_path (str): The path to the input audio file.
    message (str): The message to be encoded.
    output_path (str): The path where the encoded audio file will be saved.

    Returns:
    None

    Raises:
    ValueError: If the message is too long to encode in the given audio file.
    """
    audio = AudioSegment.from_file(audio_path)
    samples = np.array(audio.get_array_of_samples())

    message += chr(0)  # Null-terminate the message
    bin_message = ''.join(format(ord(char), '08b') for char in message)
    message_len = len(bin_message)
    audio_len = len(samples)

    if message_len > audio_len:
        raise ValueError("Message is too long to encode in this audio file.")

    for i in range(message_len):
        samples[i] = (samples[i] & ~1) | int(bin_message[i])

    encoded_audio = audio._spawn(samples.tobytes())
    encoded_audio.export(output_path, format="wav")


def decode_audio(audio_path):
    """
    This function decodes a message from an audio file using LSB steganography.

    Parameters:
    audio_path (str): The path to the input audio file.

    Returns:
    str: The decoded message.

    Raises:
    None

    Note:
    The function assumes that the message was encoded using the encode_audio function.
    """
    # Load the audio file
    audio = AudioSegment.from_file(audio_path)

    # Convert the audio samples to a numpy array
    samples = np.array(audio.get_array_of_samples())

    # Initialize an empty string to store the binary representation of the message
    bin_message = ''

    # Iterate over each sample and extract the least significant bit
    for sample in samples:
        bin_message += str(sample & 1)

    # Convert the binary representation of the message to a string
    message = ''.join(chr(int(bin_message[i:i+8], 2)) for i in range(0, len(bin_message), 8))

    # Stop at the null character (indicating the end of the message)
    return message.split(chr(0))[0]