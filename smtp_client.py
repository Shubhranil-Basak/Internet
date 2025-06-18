import socket

def send_email(sender, recipient, subject, body):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 2525))
    print(s.recv(1024).decode())

    def send(cmd):
        s.sendall((cmd + "\r\n").encode())
        print(s.recv(1024).decode())

    send(f"HELO myclient.com")
    send(f"MAIL FROM: {sender}")
    send(f"RCPT TO: <{recipient}>")
    send(f"SUBJECT: {subject}")
    send("DATA")
    for line in body.splitlines():
        s.sendall((line + "\r\n").encode())
    s.sendall(b".\r\n")
    print(s.recv(1024).decode())

    send("QUIT")
    s.close()

# Test it
send_email(
    "alice@example.com",
    "bob@example.com",
    "Meeting Reminder",
    "Don't forget our meeting at 3 PM today.\nThanks!\nAlice"
)

