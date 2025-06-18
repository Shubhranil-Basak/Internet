from email.smtp.client.core import SMTPClient

def main():
    client = SMTPClient()
    client.connect()

    sender = input("From: ")
    recipient = input("To: ")
    subject = input("Subject: ")
    print("Enter message body. End with a blank line:")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    body = "\n".join(lines)

    client.send_mail(sender, recipient, subject, body)
    client.quit()

if __name__ == "__main__":
    main()