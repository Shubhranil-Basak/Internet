from email.smtp.server.core import SMTPServer

if __name__ == "__main__":
    server = SMTPServer()
    
    print("Starting SMTP server...")
    server.socket.listen()
    print(f"SMTP Server running on port {server.port}")

    while True:
        conn, addr = server.socket.accept()
        print(f"Connection from {addr}")
        conn.sendall(b"220 Welcome to the SMTP server\r\n")
        
        sender = recipient = ""
        data_lines = []

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            
            if data.upper().startswith("RCPT TO:"):
                recipient = data.split(":", 1)[1].strip().strip("<>")
            elif data.upper().startswith("MAIL FROM:"):
                sender = data.split(":", 1)[1].strip()
            elif data.upper() == "DATA":
                conn.sendall(b"354 End with . on a line\r\n")
                buffer = ""
                while True:
                    chunk = conn.recv(1024).decode()
                    buffer += chunk
                    if "\r\n.\r\n" in buffer or "\n.\n" in buffer:
                        break
                data_body = buffer.strip().splitlines()
                if data_body[-1] == ".":
                    data_body.pop()
                content = f"From: {sender}\nTo: {recipient}\n" + "\n".join(data_body)
                server.save_email(recipient, content)
            elif data.upper() == "QUIT":
                response = server.parse_command(data)
                conn.sendall(response)
                break
            else:
                response = b"500 Command not recognized\r\n"

            response = server.parse_command(data)
            conn.sendall(response)
        
        conn.close()

        print(f"Connection from {addr} closed")