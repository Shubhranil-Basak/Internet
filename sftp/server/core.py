import socket
import threading
from .session import FTPSession

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    session = FTPSession(conn, addr)
    session.send("220 Simple FTP Server Ready\n")

    try:
        while True:
            data = session.recv()
            if not data:
                break

            session.buffer += data
            lines = session.buffer.split("\n")

            for line in lines[:-1]:
                command = line.strip()
                print(f"[{addr}] ⇨ {command}")
                response = session.process_command(command)
                session.send(response)
                if command.upper() == "QUIT":
                    conn.close()
                    return

            session.buffer = lines[-1]
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
        conn.close()

def start_server(host='localhost', port=2121):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[🔌] SFTP Server running on {host}:{port}")

    while True:
        conn, addr = server_socket.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
