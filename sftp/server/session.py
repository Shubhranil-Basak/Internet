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

    def recv(self, size=1024):
        return self.conn.recv(size).decode()

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
            return handle_get(filename)

        elif command.upper().startswith("PUT "):
            if not self.logged_in:
                return "530 Not logged in\n"
            filename = command[4:].strip()
            self.send("150 Ready to receive file\n")
            content = self.recv(4096)
            return handle_put(filename, content)

        elif command.upper() == "QUIT":
            return "221 Goodbye\n"

        else:
            return "502 Command not implemented\n"
