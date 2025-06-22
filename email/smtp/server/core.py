import os
import socket

class SMTPServer:
    def __init__(self, host='localhost', port=2525):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))


    def handle_helo(self, data):
        return b"250 Hello\r\n"

    def handle_mail_from(self, data):
        sender = data.split(":", 1)[1].strip()
        return sender, b"250 OK\r\n"

    def handle_rcpt_to(self, data):
        recipient = data.split(":", 1)[1].strip().strip("<>")
        return recipient, b"250 OK\r\n"

    def handle_data_start(self):
        return b"354 End with . on a line\r\n"

    def process_data_body(self, data_body_lines, sender, recipient, MAILBOX_DIR):
        content = f"From: {sender}\nTo: {recipient}\n" + "\n".join(data_body_lines)
        self.save_email(recipient, content, MAILBOX_DIR)
        return b"250 Message received\r\n"

    def handle_quit(self):
        return b"221 Bye\r\n"

    def handle_unknown(self):
        return b"500 Command not recognized\r\n"

    def save_email(self, recipient, content, MAILBOX_DIR):
        mailbox = os.path.join(MAILBOX_DIR, recipient)
        os.makedirs(mailbox, exist_ok=True)
        index = len(os.listdir(mailbox)) + 1
        path = os.path.join(mailbox, f"{index}.txt")
        with open(path, "w") as f:
            f.write(content)
