import socket
import threading

def parse_request(data):
    data = data.strip()
    lines = data.split("\n")
    method, path = lines[0].split()
    headers = {}
    for line in lines[1:]:
        if line.strip() == "":
            break
        key, value = line.split(": ")
        headers[key] = value
    return method, path, headers

def handle_request(method, path):
    if method == "GET" and path == "/hello":
        body = "Hello from SHTTP!"
        response = f"200 OK\nContent-Length: {len(body)}\n\n{body}"
    elif method == 'POST' and path.startswith("/hello?"):
        query = path.split("?")[1]
        params = dict(param.split('=') for param in query.split('&'))
        response = f'200 OK\nContent-Type: text/plain\n\nHello {params.get("name", "World")}\nYour age is {params.get("age", "unknown")}.'
    else:
        body = "Not Found"
        response = f"404 Not Found\nContent-Length: {len(body)}\n\n{body}"
    return response

def handle_client(conn, addr):
    print(f"[+] New connection from {addr}")
    conn.settimeout(60)  # optional: timeout idle connections

    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break

            decoded = data.decode()
            if decoded.strip() == "":
                continue

            method, path, headers = parse_request(decoded)
            response = handle_request(method, path)

            conn.sendall(response.encode())

            # Break if the client signals to close
            if headers.get("Connection", "").lower() == "close":
                print(f"[-] Closing connection to {addr}")
                break
    except socket.timeout:
        print(f"[!] Connection to {addr} timed out.")
    except Exception as e:
        print(f"[!] Error with client {addr}: {e}")
    finally:
        conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('localhost', 8081))
    s.listen()
    print("SHTTP Server running on port 8081 (Ctrl+C to stop)")

    try:
        while True:
            conn, addr = s.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("\n[!] Server shutting down.")
        s.close()

start_server()
