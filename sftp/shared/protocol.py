def format_response(code: int, message: str, data: str = "") -> str:
    return f"{code} {message}\n{data}"

def parse_response(response: str):
    lines = response.strip().split("\n")
    status_line = lines[0]
    code, message = status_line.split(" ", 1)
    body = "\n".join(lines[1:]) if len(lines) > 1 else ""
    return {
        "code": int(code),
        "message": message,
        "body": body
    }
