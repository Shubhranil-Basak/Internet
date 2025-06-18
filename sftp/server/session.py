from .auth import authenticate
from .commands import handle_list, handle_get, handle_put

class FTPSession:
    def __init__(self, conn, addr):
        self.conn = conn
        self.addr = addr
        self.username = None
        self.logged_in = False
        self.buffer = ""

    def send(self, msg):
        self.conn.sendall(msg.encode())
    
    def send_bytes(self, data: bytes):
        self.conn.sendall(data)

    def recv(self, size=1024, raw=False):
        data = self.conn.recv(size)
        return data if raw else data.decode()
    
    def process_command(self, command):
        if command.upper().startswith("USER "):
            self.username = command[5:].strip()
            return "331 Username OK, need password\n"

        elif command.upper().startswith("PASS "):
            password = command[5:].strip()
            if authenticate(self.username, password):
                self.logged_in = True
                return "230 Login successful\n"
            else:
                return "530 Login incorrect\n"

        elif command.upper() == "LIST":
            if not self.logged_in:
                return "530 Not logged in\n"
            return handle_list()

        elif command.upper().startswith("GET "):
            if not self.logged_in:
                return "530 Not logged in\n"
            filename = command[4:].strip()
            self.send_bytes(handle_get(filename))
            return ""

        elif command.upper().startswith("PUT "):
            if not self.logged_in:
                return "530 Not logged in\n"
            filename = command[4:].strip()
            self.send("150 Ready to receive file\n")

            # Receive file size first
            size_line = self.recv()
            try:
                file_size = int(size_line.strip())
            except ValueError:
                return "550 Invalid file size\n"

            file_data = b''
            while len(file_data) < file_size:
                chunk = self.recv(min(4096, file_size - len(file_data)), raw=True)
                if not chunk:
                    break
                file_data += chunk

            return handle_put(filename, file_data)

        elif command.upper() == "QUIT":
            return "221 Goodbye\n"

        else:
            return "502 Command not implemented\n"
