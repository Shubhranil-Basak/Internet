import os
import socket
from .auth import authenticate

MAILBOX_DIR = "mailboxes"

class POP3Server:
    def __init__(self, host='localhost', port=1100):
        self.host = host
        self.port = port

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        print(f"POP3 Server running on {self.port}")

        while True:
            conn, addr = s.accept()
            self.handle_client(conn)

    def handle_client(self, conn):
        conn.sendall(b"+OK Simple POP3 Server Ready\r\n")
        user_email = ""
        authenticated = False

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split()
            cmd = parts[0].upper()

            if cmd == "USER":
                if len(parts) < 2:
                    conn.sendall(b"-ERR Missing email\r\n")
                else:
                    user_email = parts[1]
                    mailbox = os.path.join(MAILBOX_DIR, user_email)
                    if os.path.exists(mailbox):
                        conn.sendall(b"+OK User accepted\r\n")
                    else:
                        conn.sendall(b"-ERR Mailbox not found\r\n")
            elif cmd == "PASS":
                if user_email:
                    authenticated = authenticate(user_email, parts[1])
                    if authenticated:
                        conn.sendall(b"+OK Authenticated\r\n")
                    else:
                        conn.sendall(b"-ERR Authentication failed\r\n")
                        break
                else:
                    conn.sendall(b"-ERR USER required first\r\n")
            elif cmd == "LIST":
                if not authenticated:
                    conn.sendall(b"-ERR Authenticate first\r\n")
                    continue
                mailbox = os.path.join(MAILBOX_DIR, user_email)
                files = sorted(os.listdir(mailbox))
                conn.sendall(f"+OK {len(files)} messages\r\n".encode())
                for i, f in enumerate(files, 1):
                    size = os.path.getsize(os.path.join(mailbox, f))
                    conn.sendall(f"{i} {size}\r\n".encode())
                conn.sendall(b".\r\n")
            elif cmd == "RETR":
                if not authenticated or len(parts) < 2:
                    conn.sendall(b"-ERR Usage: RETR <number>\r\n")
                    continue
                msg_num = int(parts[1])
                mailbox = os.path.join(MAILBOX_DIR, user_email)
                files = sorted(os.listdir(mailbox))
                if msg_num < 1 or msg_num > len(files):
                    conn.sendall(b"-ERR Message not found\r\n")
                    continue
                with open(os.path.join(mailbox, files[msg_num - 1]), "r") as f:
                    content = f.read()
                conn.sendall(b"+OK Message follows\r\n")
                conn.sendall(content.encode())
                conn.sendall(b"\r\n.\r\n")
            elif cmd == "QUIT":
                conn.sendall(b"+OK Goodbye\r\n")
                break
            else:
                conn.sendall(b"-ERR Unknown command\r\n")

        conn.close()
