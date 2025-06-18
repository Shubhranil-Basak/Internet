def read_binary_file(filename: str) -> bytes:
    """Read a file in binary mode and return bytes"""
    with open(filename, "rb") as f:
        return f.read()

def write_binary_file(filename: str, content: bytes):
    """Write binary content to a file"""
    with open(filename, "wb") as f:
        f.write(content)