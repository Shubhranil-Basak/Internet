from .core import FTPClient
from .utils import read_file, write_file

def main():
    client = FTPClient()
    client.connect()

    while True:
        command = input("SFTP > ").strip()

        if command.upper() == "QUIT":
            res = client.send_command(command)
            print(res['message'])
            client.close()
            break

        elif command.upper().startswith("PUT "):
            filename = command[4:].strip()
            try:
                data = read_file(filename)
                res = client.send_command(command, data)
                print(res['message'])
            except FileNotFoundError:
                print("Local file not found.")

        elif command.upper().startswith("GET "):
            filename = command[4:].strip()
            res = client.send_command(command)
            if res["code"] == 200:
                write_file(filename, res["body"])
                print(f"File '{filename}' downloaded.")
            else:
                print(res["message"])

        else:
            res = client.send_command(command)
            print(res["message"])
            if res["body"]:
                print(res["body"])

if __name__ == "__main__":
    main()
