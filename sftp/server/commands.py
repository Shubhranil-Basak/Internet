import os
from .config import FILE_DIR

def handle_list():
    files = os.listdir(FILE_DIR)
    return "200 OK\n" + "\n".join(files) + "\n"

def handle_get(filename):
    filepath = os.path.join(FILE_DIR, filename)
    if os.path.isfile(filepath):
        with open(filepath, "rb") as f:
            content = f.read()
        header = f"200 OK\n{len(content)}\n".encode()
        return header + content
    else:
        return b"550 File not found\n"

def handle_put(filename, file_data):
    filepath = os.path.join(FILE_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file_data)
    return "226 File upload complete\n"
