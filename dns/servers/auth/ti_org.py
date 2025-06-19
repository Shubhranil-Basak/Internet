from dns.core import DNSServer

if __name__ == "__main__":
    server = DNSServer("dns/zones/ti.org.json", port=6003)
    server.start()
