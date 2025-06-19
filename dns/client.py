import socket

ROOT_DNS_HOST = "localhost"
ROOT_DNS_PORT = 5353

def send_query(command: str):
    try:
        with socket.socket() as s:
            s.connect((ROOT_DNS_HOST, ROOT_DNS_PORT))
            s.sendall((command + "\n").encode())
            response = s.recv(1024).decode().strip()
            return response
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🌐 DNS CLI Client (Connected to ROOT DNS)")
    print("Commands:")
    print("  RESOLVE <domain>")
    print("  REVERSE <ip>")
    print("  EXIT")

    while True:
        try:
            cmd = input("DNS > ").strip()
            if cmd.upper() == "EXIT":
                break
            elif cmd:
                response = send_query(cmd)
                print(f"📥 Response: {response}")
        except KeyboardInterrupt:
            break

    print("✅ Client closed.")

if __name__ == "__main__":
    main()
