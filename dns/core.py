import socket
import threading
import json
import os
from dns.utils import forward_query

class DNSServer:
    def __init__(self, zone_file, host='localhost', port=5353):
        self.host = host
        self.port = port
        self.zone_file = zone_file
        self.records = self.load_zone()

    def load_zone(self):
        if os.path.exists(self.zone_file):
            with open(self.zone_file, 'r') as f:
                return json.load(f)
        return {}

    def save_zone(self):
        with open(self.zone_file, 'w') as f:
            json.dump(self.records, f, indent=2)

    def handle_request(self, data):
        parts = data.strip().split()
        if not parts:
            return "400 Bad Request"

        cmd = parts[0].upper()

        if cmd == "RESOLVE":
            domain = parts[1]
            return self.resolve(domain)

        elif cmd == "REVERSE":
            ip = parts[1]
            return self.reverse(ip)

        return "400 Unknown Command"

    def resolve(self, domain):
        # Step 1: Try full match
        if domain in self.records:
            entry = self.records[domain]
            if isinstance(entry, dict) and "ip" in entry:
                return f"200 FOUND {entry['ip']}"
            elif isinstance(entry, dict) and "forward" in entry:
                next_host, next_port = entry["forward"]
                print(f"🔁 Forwarding {domain} to {next_host}:{next_port}")
                return forward_query(domain, next_host, next_port)

        # Step 2: Try suffix match for delegation (like .com)
        parts = domain.split('.')
        for i in range(1, len(parts)):
            suffix = '.'.join(parts[i:])  # example.com, com, etc.
            if suffix in self.records and isinstance(self.records[suffix], dict):
                forward = self.records[suffix].get("forward")
                if forward:
                    next_host, next_port = forward
                    print(f"🔁 Forwarding {domain} to {next_host}:{next_port} via suffix match {suffix}")
                    return forward_query(domain, next_host, next_port)

        return "404 NOT FOUND"


    def reverse(self, ip):
        for domain, data in self.records.items():
            if isinstance(data, dict) and data.get("ip") == ip:
                return f"200 FOUND {domain}"
        return "404 NOT FOUND"

    def start(self):
        s = socket.socket()
        s.bind((self.host, self.port))
        s.listen()
        print(f"DNS Server listening on {self.host}:{self.port}")

        while True:
            conn, _ = s.accept()
            threading.Thread(target=self.handle_connection, args=(conn,)).start()

    def handle_connection(self, conn):
        try:
            data = conn.recv(1024).decode()
            print(f"[{self.__class__.__name__}] Request: {data.strip()}")
            response = self.handle_request(data)
            conn.sendall((response + "\n").encode())
        finally:
            conn.close()
