import cv2
import socket
import time
import argparse
import struct
import random

MAX_PACKET_SIZE = 65000  # UDP safe limit

def start_udp_video_server(host='127.0.0.1', port=9000, use_webcam=True, file_path=None):
    cap = cv2.VideoCapture(0 if use_webcam else file_path)

    if not cap.isOpened():
        print("Unable to open video source.")
        return

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))  # Required for recvfrom
    print(f"UDP Video Server started on {host}:{port}")

    print("Waiting for client to connect...")
    data, client_addr = sock.recvfrom(1024)
    print(f"Client connected from {client_addr}")

    frame_id = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        _, buffer = cv2.imencode('.jpg', frame)
        data = buffer.tobytes()

        packet = struct.pack(">I", frame_id) + data[:65000 - 4]
        sock.sendto(packet, client_addr)

        if random.random() < 0.05:
            print("buffering")
            time.sleep(random.uniform(0.1, 0.2))

        frame_id += 1
        time.sleep(1 / 30)

    cap.release()
    sock.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--file", help="Video file path")
    args = parser.parse_args()

    start_udp_video_server(
        host=args.host,
        port=args.port,
        use_webcam=(args.file is None),
        file_path=args.file
    )
