from email.pop3.client.core import POP3Client

def main():
    client = POP3Client()
    client.connect()

    email = input("Email: ")
    password = input("Password: ")
    is_connected = client.login(email, password)

    # Check if the server has closed the connection
    if is_connected:
        messages = client.list_messages()
        print("\nMessages:")
        for line in messages:
            print(line)

        while True:
            msg_num = input("\nEnter message number to read (or press Enter to skip): ")
            if msg_num.isdigit():
                print("\n--- Message Content ---")
                print(client.get_message(int(msg_num)))
            elif msg_num == "":
                print("Exiting...")
                break

        client.quit()

if __name__ == "__main__":
    main()