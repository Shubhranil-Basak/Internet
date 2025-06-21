import cv2
import socket
import numpy as np
import argparse
import struct
import threading
import time
from collections import deque

BUFFER_SIZE = 10  # Number of frames to buffer before playback

def start_udp_video_client(server_ip='127.0.0.1', port=9000):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(b"HELLO", (server_ip, port))  # Handshake

    frame_buffer = deque(maxlen=BUFFER_SIZE)
    running = True

    def receive_frames():
        while running:
            try:
                data, _ = sock.recvfrom(65536)
                frame_id = struct.unpack(">I", data[:4])[0]
                frame = np.frombuffer(data[4:], dtype=np.uint8)
                frame_buffer.append((frame_id, frame))
            except Exception as e:
                print(f"Error receiving frame: {e}")
                break

    recv_thread = threading.Thread(target=receive_frames)
    recv_thread.start()

    print("Playing video...")
    last_id = -1

    while running:
        if frame_buffer:
            frame_id, data = frame_buffer.popleft()
            if frame_id <= last_id:
                continue  # Drop duplicate/old frames
            last_id = frame_id

            img = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if img is not None:
                cv2.imshow("UDP Video Stream", img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    running = False
    recv_thread.join()
    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--server", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    args = parser.parse_args()

    start_udp_video_client(args.server, args.port)
