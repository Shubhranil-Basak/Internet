import socket

class POP3Client:
    def __init__(self, host='localhost', port=1100):
        self.host = host
        self.port = port
        self.conn = None
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))

    def connect(self):
        print(self.conn.recv(1024).decode().strip())

    def login(self, email, password):
        self.conn.sendall(f"USER {email}\r\n".encode())
        print(self.conn.recv(1024).decode().strip())
        self.conn.sendall(f"PASS {password}\r\n".encode())
        a = self.conn.recv(1024).decode().strip()
        return a.startswith("+OK")

    def list_messages(self):
        self.conn.sendall(b"LIST\r\n")
        lines = []
        while True:
            chunk = self.conn.recv(1024).decode()
            lines.extend(chunk.splitlines())
            if any(line.strip() == "." for line in lines):
                break
        return lines

    def get_message(self, msg_num):
        self.conn.sendall(f"RETR {msg_num}\r\n".encode())
        data = ""
        while True:
            chunk = self.conn.recv(1024).decode()
            data += chunk
            if "\r\n.\r\n" in data or "\n.\n" in data:
                break
        return data.replace("\r\n.\r\n", "").replace("\n.\n", "").strip()

    def quit(self):
        self.conn.sendall(b"QUIT\r\n")
        print(self.conn.recv(1024).decode().strip())
        self.conn.close()
