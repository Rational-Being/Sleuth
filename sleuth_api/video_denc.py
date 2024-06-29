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
