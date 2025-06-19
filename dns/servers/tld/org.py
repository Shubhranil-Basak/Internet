from dns.core import DNSServer

if __name__ == "__main__":
    server = DNSServer("dns/zones/org.json", port=6002)
    server.start()
