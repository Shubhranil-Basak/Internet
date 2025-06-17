import socket

def send_requests():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('localhost', 8081))

    while True:
        path = input("Enter path to request (e.g., /hello or 'quit'): ")
        if path.lower() == "quit":
            request = "GET /hello\nConnection: close\n\n"
            s.sendall(request.encode())
            print(s.recv(1024).decode())
            break

        request = f"GET {path}\nConnection: keep-alive\n\n"
        s.sendall(request.encode())
        response = s.recv(1024).decode()
        print("Server response:\n", response)

    s.close()

send_requests()
