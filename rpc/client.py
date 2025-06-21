import socket
import os
from protocol import send_message, receive_message, send_file

def start_client(server_ip='127.0.0.1', port=8888):
    with socket.socket() as s:
        s.connect((server_ip, port))
        print("Connected to RPC server")
        while True:
            cmd = input("RPC > ").strip()
            if cmd.lower().startswith("upload_and_run"):
                try:
                    _, filepath = cmd.split(maxsplit=1)
                    if not os.path.exists(filepath):
                        print("File does not exist.")
                        continue
                    filename = os.path.basename(filepath)
                    send_message(s, f"upload_and_run {filename}")
                    send_file(s, filepath)
                    response = receive_message(s)
                    print(response)
                except Exception as e:
                    print(f"Error: {e}")
            else:
                send_message(s, cmd)
                if cmd.lower() == "exit":
                    break
                response = receive_message(s)
                print(response)

if __name__ == "__main__":
    start_client()
