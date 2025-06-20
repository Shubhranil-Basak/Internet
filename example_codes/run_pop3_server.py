from email.pop3.server.core import POP3Server

if __name__ == "__main__":
    server = POP3Server()
    server.start()