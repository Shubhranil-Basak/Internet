from dns.core import DNSServer

if __name__ == "__main__":
    server = DNSServer("dns/zones/apple.com.json", port=6001)
    server.start()
