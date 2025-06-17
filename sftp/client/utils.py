def read_file(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read()

def write_file(filename: str, content: str):
    with open(filename, "w") as f:
        f.write(content)
