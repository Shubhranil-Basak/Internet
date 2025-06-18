from sftp.client.core import FTPClient
from sftp.client.utils import read_binary_file, write_binary_file

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
                data = read_binary_file(filename)
                res = client.send_command(command, data)
                print(res['message'])
            except FileNotFoundError:
                print("Local file not found.")
            except Exception as e:
                print(f"Error uploading file: {e}")

        elif command.upper().startswith("GET "):
            filename = command[4:].strip()
            try:
                res = client.send_command(command)
                if res["code"] == 200:
                    file_data = res["body"]
                    write_binary_file(filename, file_data)
                    print(f"File '{filename}' downloaded successfully.")
                else:
                    print(res["message"])
            except Exception as e:
                print(f"Error downloading file: {e}")

        else:
            res = client.send_command(command)
            print(res["message"])
            if res["body"]:
                print(res["body"])

if __name__ == "__main__":
    main()