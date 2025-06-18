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

    def send_command(self, command: str, file_data: bytes = None) -> dict:
        self.conn.sendall((command + "\n").encode())

        if command.upper().startswith("PUT ") and file_data:
            ack = self.conn.recv(1024).decode()
            if not ack.startswith("150"):
                return {"code": 550, "message": "Upload rejected"}
            
            self.conn.sendall(f"{len(file_data)}\n".encode())
            
            self.conn.sendall(file_data)
            
            response = self.conn.recv(4096).decode(errors="ignore")
            return parse_response(response)
        
        elif command.upper().startswith("GET "):
            header = b""
            newline_count = 0
            while newline_count < 2:
                chunk = self.conn.recv(1)
                if not chunk:
                    break
                header += chunk
                if chunk == b"\n":
                    newline_count += 1
            
            response_text = header.decode().strip()
            parsed_response = parse_response(response_text)
            
            if parsed_response["code"] != 200:
                return parsed_response
            
            try:
                file_size = int(parsed_response["body"])
            except (ValueError, TypeError):
                return {"code": 500, "message": "Invalid file size in response"}
            
            file_data = self.receive_binary_file(file_size)
            
            return {
                "code": 200,
                "message": "File received successfully",
                "body": file_data
            }
        else:
            response = self.conn.recv(1024).decode()
            return parse_response(response)

    def receive_binary_file(self, expected_size: int) -> bytes:
        """Receive binary file data of specified size"""
        buffer = b''
        while len(buffer) < expected_size:
            remaining = expected_size - len(buffer)
            chunk_size = min(4096, remaining)
            chunk = self.conn.recv(chunk_size)
            if not chunk:
                break
            buffer += chunk
        return buffer

    def close(self):
        if self.conn:
            self.conn.close()