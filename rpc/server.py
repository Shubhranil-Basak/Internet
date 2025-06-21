import socket
import subprocess
import os
from protocol import send_message, receive_message, receive_file

UPLOAD_DIR = "uploads"

def handle_client(conn, addr):
    print(f"Client connected: {addr}")
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    while True:
        cmd = receive_message(conn)
        if not cmd or cmd.strip().lower() == "exit":
            print("Client disconnected.")
            break

        if cmd.startswith("upload_and_run"):
            _, filename = cmd.strip().split(maxsplit=1)
            save_path = os.path.join(UPLOAD_DIR, filename)
            print(f"Receiving file: {filename}")
            if receive_file(conn, save_path):
                try:
                    print(f"Executing {filename}")
                    output = subprocess.check_output(f"python3 {save_path}", shell=True, stderr=subprocess.STDOUT, text=True)
                except subprocess.CalledProcessError as e:
                    output = e.output
                send_message(conn, output)
            else:
                send_message(conn, "File transfer failed.")
        else:
            print(f"Command received: {cmd}")
            try:
                output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                output = e.output
            send_message(conn, output)

def start_server(host='0.0.0.0', port=8888):
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        print(f"RPC Server running on {host}:{port}")
        conn, addr = s.accept()
        with conn:
            handle_client(conn, addr)

if __name__ == "__main__":
    start_server()
