from email.smtp.server.core import SMTPServer

MAILBOX_DIR = "mailboxes"

if __name__ == "__main__":
    server = SMTPServer()
    server.socket.listen()
    print(f"SMTP server listening on {server.host}:{server.port}")
    
    while True:
        conn, addr = server.socket.accept()
        print("done")
        print(f"Connection from {addr}")
        conn.sendall(b"220")

        sender = ""
        recipient = ""

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            data_upper = data.upper()

            if data_upper.startswith("HELO"):
                response = server.handle_helo(data)

            elif data_upper.startswith("MAIL FROM:"):
                sender, response = server.handle_mail_from(data)

            elif data_upper.startswith("RCPT TO:"):
                recipient, response = server.handle_rcpt_to(data)

            elif data_upper == "DATA":
                conn.sendall(server.handle_data_start())
                buffer = ""
                while True:
                    chunk = conn.recv(1024).decode()
                    buffer += chunk
                    if "\r\n.\r\n" in buffer or "\n.\n" in buffer:
                        break
                data_body = buffer.strip().splitlines()
                if data_body[-1] == ".":
                    data_body.pop()
                response = server.process_data_body(data_body, sender, recipient)

            elif data_upper == "QUIT":
                response = server.handle_quit()
                conn.sendall(response)
                break

            else:
                response = server.handle_unknown()

            conn.sendall(response)

        conn.close()
        print(f"Connection from {addr} closed")
