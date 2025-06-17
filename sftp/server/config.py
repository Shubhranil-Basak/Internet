import os

USERS = {
    "admin": "1234",
    "john": "hunter2"
}

FILE_DIR = "sftp_files"
os.makedirs(FILE_DIR, exist_ok=True)
