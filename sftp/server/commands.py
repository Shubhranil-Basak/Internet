import os
from .config import FILE_DIR

def handle_list():
    files = os.listdir(FILE_DIR)
    return "200 OK\n" + "\n".join(files) + "\n"

def handle_get(filename):
    filepath = os.path.join(FILE_DIR, filename)
    if os.path.isfile(filepath):
        with open(filepath, "r") as f:
            content = f.read()
        return f"200 OK\n{content}\n"
    else:
        return "550 File not found\n"

def handle_put(filename, content):
    filepath = os.path.join(FILE_DIR, filename)
    with open(filepath, "w") as f:
        f.write(content)
    return "226 File upload complete\n"
