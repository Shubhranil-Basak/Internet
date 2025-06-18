import os

MAILBOX_DIR = "mailboxes"

def ensure_mailbox(email):
    path = os.path.join(MAILBOX_DIR, email)
    os.makedirs(path, exist_ok=True)
    return path

def list_emails(email):
    mailbox = ensure_mailbox(email)
    return sorted(os.listdir(mailbox))

def save_email(email, content: str):
    mailbox = ensure_mailbox(email)
    idx = len(os.listdir(mailbox)) + 1
    path = os.path.join(mailbox, f"{idx}.txt")
    with open(path, "w") as f:
        f.write(content)
