import socket
import threading
from .protocol import parse_request, build_response

class SHTTPServer:
    def __init__(self, host, port, router):
        self.host = host
        self.port = port
        self.router = router

    def handle_client(self, conn, addr):
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    break

                request = parse_request(data.decode())
                print(request)
                method = request["method"]
                path = request["path"]
                body = request["body"]

                status, message, headers, response_body = self.router.handle(method, path, body)
                response = build_response(status, message, headers, response_body)

                conn.sendall(response.encode())

                if request["headers"].get("Connection", "").lower() == "close":
                    break
        finally:
            conn.close()

    def start(self):
        print(f"Starting SHTTP server on {self.host}:{self.port}")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((self.host, self.port))
        s.listen()

        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except KeyboardInterrupt:
            print("\nServer shutting down.")
        finally:
            s.close()
