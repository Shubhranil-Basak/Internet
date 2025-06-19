from dns.core import DNSServer

if __name__ == "__main__":
    server = DNSServer("dns/zones/com.json", port=6000)
    server.start()
