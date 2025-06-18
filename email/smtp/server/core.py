import os
import socket

MAILBOX_DIR = "mailboxes"

class SMTPServer:
    def __init__(self, host='localhost', port=2525):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))


    def parse_command(self, data):

            if data.upper().startswith("HELO"):
                return b"250 Hello\r\n"
            
            elif data.upper().startswith("MAIL FROM:"):
                return b"250 OK\r\n"
            
            elif data.upper().startswith("RCPT TO:"):
                return b"250 OK\r\n"
            
            elif data.upper() == "DATA":
                return b"250 Message received\r\n"
            
            elif data.upper() == "QUIT":
                return b"221 Bye\r\n"

    def save_email(self, recipient, content):
        mailbox = os.path.join(MAILBOX_DIR, recipient)
        os.makedirs(mailbox, exist_ok=True)
        index = len(os.listdir(mailbox)) + 1
        path = os.path.join(mailbox, f"{index}.txt")
        with open(path, "w") as f:
            f.write(content)