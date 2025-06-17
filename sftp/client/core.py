import socket
from sftp.shared.protocol import parse_response

class FTPClient:
    def __init__(self, host='localhost', port=2121):
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        welcome = self.conn.recv(1024).decode().strip()
        print(welcome)

    def send_command(self, command: str, file_data: str = None):
        self.conn.sendall((command + "\n").encode())

        if command.upper().startswith("PUT ") and file_data:
            self.conn.recv(1024)
            self.conn.sendall(file_data.encode())

        response = self.conn.recv(4096).decode()
        return parse_response(response)

    def close(self):
        self.conn.close()
