import os
import socket
from .auth import authenticate as auth


class POP3Server:
    def __init__(self, host='localhost', port=1100):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))

    def handle_handshake(self, conn):
        conn.sendall(b"+OK Simple POP3 Server Ready\r\n")
    
    def handle_user(self, conn, parts, MAILBOX_DIR):
        user_email = parts[1]
        mailbox = os.path.join(MAILBOX_DIR, user_email)
        if os.path.exists(mailbox):
            conn.sendall(b"+OK User accepted\r\n")
        else:
            conn.sendall(b"-ERR Mailbox not found\r\n")
        
        return user_email, mailbox
    
    def authinticate(self, user_email, parts):
        return auth(user_email, parts[1])
    
    def handle_authenticated(self, conn, authenticated):
        if authenticated:
            conn.sendall(b"+OK Authenticated\r\n")
        else:
            conn.sendall(b"-ERR Authentication failed\r\n")
    
    def handle_no_user(self, conn):
        conn.sendall(b"-ERR USER required first\r\n")

    def list(self, conn, mailbox):
        files = sorted(os.listdir(mailbox))
        conn.sendall(f"+OK {len(files)} messages\r\n".encode())
        for i, f in enumerate(files, 1):
            size = os.path.getsize(os.path.join(mailbox, f))
            conn.sendall(f"{i} {size}\r\n".encode())
        conn.sendall(b".\r\n")
    
    def handle_retr(self, conn, parts, mailbox):
        msg_num = int(parts[1])
        files = sorted(os.listdir(mailbox))

        if msg_num < 1 or msg_num > len(files):
            conn.sendall(b"-ERR Message not found\r\n")
            return
        
        with open(os.path.join(mailbox, files[msg_num - 1]), "r") as f:
            content = f.read()
        return content.encode()
    
    def send_content(self, conn, content):
        conn.sendall(content + b"\r\n.\r\n")
    
    def send_EOF(self, conn):
        conn.sendall(b".\r\n")
    
    def handle_quit(self, conn):
        conn.sendall(b"+OK Goodbye\r\n")

    def handle_unknown_command(self, conn):
        conn.sendall(b"-ERR Unknown command\r\n")