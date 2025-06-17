import socket
from .protocol import parse_response

class SHTTPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((host, port))

    def send_request(self, method, path, headers=None, body=""):
        headers = headers or {}
        headers.setdefault("Connection", "keep-alive")

        request = f"{method} {path}\n" + "\n".join(f"{k}: {v}" for k, v in headers.items()) + "\n\n" + body
        self.socket.sendall(request.encode())
        response = self.socket.recv(1024).decode()
        return parse_response(response)

    def close(self):
        self.socket.close()
