from shttp.client.core import SHTTPClient

def main():
    client = SHTTPClient("localhost", 8081)
    print("🔗 Connected to SHTTP Server (localhost:8081)")
    print("Type 'exit' to quit.\n")

    try:
        while True:
            method = input("Method (GET/POST): ").strip().upper()
            if method == "EXIT":
                break
            if method not in ["GET", "POST"]:
                print("❌ Invalid method. Use GET or POST.")
                continue

            path = input("Path (e.g., /hello): ").strip()
            if not path.startswith("/"):
                print("❌ Path should start with '/'.")
                continue

            headers = {}
            body = ""

            if method == "GET":
                params = input("Query params (e.g., name=John&age=20): ").strip()
                if params:
                    path += "?" + params
            elif method == "POST":
                body = input("POST body (plain text): ").strip()

            headers["Connection"] = input("Connection type (keep-alive/close) [default: keep-alive]: ").strip() or "keep-alive"

            response = client.send_request(method, path, headers, body)
            print("\n📥 Response:")
            print(response)
            print("-" * 40)
            
            if headers["Connection"].lower() == "close":
                print("🔌 Closing connection.")
                break

    finally:
        client.close()
        print("✅ Client closed.")

if __name__ == "__main__":
    main()
