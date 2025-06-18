import socket

class SMTPClient:
    def __init__(self, host='localhost', port=2525):
        self.host = host
        self.port = port
        self.conn = None

    def connect(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.host, self.port))
        print(self.conn.recv(1024).decode().strip())

    def send_mail(self, sender, recipient, subject, body):
        self.conn.sendall(f"HELO client\r\n".encode())
        self.conn.recv(1024)

        self.conn.sendall(f"MAIL FROM: {sender}\r\n".encode())
        self.conn.recv(1024)

        self.conn.sendall(f"RCPT TO: {recipient}\r\n".encode())
        self.conn.recv(1024)

        self.conn.sendall(b"DATA\r\n")
        self.conn.recv(1024)

        message = f"Subject: {subject}\r\n{body}\r\n.\r\n"
        self.conn.sendall(message.encode())
        print(self.conn.recv(1024).decode().strip())

    def quit(self):
        self.conn.sendall(b"QUIT\r\n")
        print(self.conn.recv(1024).decode().strip())
        self.conn.close()