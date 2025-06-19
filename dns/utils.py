import socket
import os
import json

def forward_query(query, host, port):
    try:
        s = socket.socket()
        s.connect((host, port))
        s.sendall((f"RESOLVE {query}\n").encode())
        response = s.recv(1024).decode().strip()
        return response
    except:
        return "502 DNS Forwarding Error"

PORT_TRACKER_FILE = os.path.join("dns", "zones", "ports.json")
START_PORT = 6000

def get_next_free_port():
    if not os.path.exists(PORT_TRACKER_FILE):
        with open(PORT_TRACKER_FILE, "w") as f:
            json.dump({"last_port": START_PORT}, f)

    with open(PORT_TRACKER_FILE, "r") as f:
        data = json.load(f)

    port = data["last_port"]
    data["last_port"] += 1

    with open(PORT_TRACKER_FILE, "w") as f:
        json.dump(data, f)

    return port
