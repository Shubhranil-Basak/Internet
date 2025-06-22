from email.pop3.server.core import POP3Server

MAILBOX_DIR = "mailboxes"

if __name__ == "__main__":
    server = POP3Server()
    server.socket.listen()
    print(f"POP3 server listening on {server.host}:{server.port}")
    
    
    while True:
        conn, addr = server.socket.accept()
        print(f"Connection from {addr}")
        
        server.handle_handshake(conn)

        user_email = ""
        authenticated = False
        mailbox = ""

        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break

            parts = data.split()
            cmd = parts[0].upper()

            cmd_upper = cmd.upper()

            if cmd_upper == "USER":
                if len(parts) < 2:
                    conn.sendall(b"-ERR Missing email\r\n")
                else:
                    user_email, mailbox = server.handle_user(conn, parts, MAILBOX_DIR)
            
            elif cmd_upper == "PASS":
                if user_email:
                    authenticated = server.authinticate(user_email, parts)
                    server.handle_authenticated(conn, authenticated)
                else:
                    server.handle_no_user(conn)
            
            elif cmd_upper == "LIST":
                if not authenticated:
                    conn.sendall(b"-ERR Authenticate first\r\n")
                    continue
                server.list(conn, mailbox)
            
            elif cmd_upper == "RETR":
                if not authenticated or len(parts) < 2:
                    conn.sendall(b"-ERR Usage: RETR <number>\r\n")
                    continue
                content = server.handle_retr(conn, parts, mailbox)
                if content:
                    server.send_content(conn, content)
                else:
                    conn.sendall(b"-ERR Message not found\r\n")

            elif cmd_upper == "QUIT":
                server.handle_quit(conn)
                break
            else:
                server.handle_unknown_command(conn)

        conn.close()
        print(f"Connection from {addr} closed")