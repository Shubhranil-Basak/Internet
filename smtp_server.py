import socket
import threading
import os

MAILBOX_DIR = "mailboxes"

def handle_client(conn, addr):
    conn.sendall(b"220 Simple SMTP Ready\r\n")
    sender = recipient = ""
    data_lines = []

    while True:
        data = conn.recv(1024).decode().strip()
        if not data:
            break

        if data.upper().startswith("HELO"):
            conn.sendall(b"250 Hello\r\n")
        elif data.upper().startswith("MAIL FROM:"):
            sender = data.split(":", 1)[1].strip()
            conn.sendall(b"250 OK\r\n")
        elif data.upper().startswith("RCPT TO:"):
            recipient = data.split(":", 1)[1].strip().strip('<>')
            conn.sendall(b"250 OK\r\n")
        elif data.upper().startswith("SUBJECT:"):
            subject = data.split(":", 1)[1].strip()
            conn.sendall(b"250 OK\r\n")
        elif data.upper() == "DATA":
            conn.sendall(b"354 End with . on a line\r\n")
            data_lines = []
            while True:
                line = conn.recv(1024).decode()
                if not line:
                    break
                # Split into lines in case multiple lines are received at once
                for l in line.splitlines():
                    if l == ".":
                        break
                    data_lines.append(l)
                if "." in line.splitlines():
                    break
            # Save email
            recipient_dir = os.path.join(MAILBOX_DIR, recipient)
            os.makedirs(recipient_dir, exist_ok=True)
            email_count = len(os.listdir(recipient_dir)) + 1
            email_path = os.path.join(recipient_dir, f"{email_count}.txt")

            with open(email_path, "w") as f:
                f.write(f"From: {sender}\nTo: {recipient}\nSubject: {subject}\n" + "\n".join(data_lines) + "\n")
                
            conn.sendall(b"250 Message received\r\n")
        elif data.upper() == "QUIT":
            conn.sendall(b"221 Bye\r\n")
            break
        else:
            conn.sendall(b"500 Command not recognized\r\n")

    conn.close()

def start_smtp_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', 2525))
    s.listen()
    print("SMTP Server running on port 2525")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

start_smtp_server()
