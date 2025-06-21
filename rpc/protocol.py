import struct

def send_message(sock, message: str):
    data = message.encode()
    length = struct.pack(">I", len(data))
    sock.sendall(length + data)

def receive_message(sock):
    length_bytes = sock.recv(4)
    if not length_bytes:
        return None
    length = struct.unpack(">I", length_bytes)[0]
    return sock.recv(length).decode()

def send_file(sock, filename: str):
    with open(filename, "rb") as f:
        data = f.read()
    length = struct.pack(">I", len(data))
    sock.sendall(length + data)

def receive_file(sock, save_path: str):
    length_bytes = sock.recv(4)
    if not length_bytes:
        return False
    length = struct.unpack(">I", length_bytes)[0]
    data = b''
    while len(data) < length:
        packet = sock.recv(length - len(data))
        if not packet:
            return False
        data += packet
    with open(save_path, "wb") as f:
        f.write(data)
    return True
