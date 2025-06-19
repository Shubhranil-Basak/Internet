from dns.core import DNSServer

if __name__ == "__main__":
    server = DNSServer("dns/zones/root.json", port=5353)
    server.start()