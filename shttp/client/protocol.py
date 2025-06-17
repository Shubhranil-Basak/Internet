def parse_response(data):
    lines = data.strip().split("\n")
    status_code, status_message = lines[0].split(" ", 1)
    headers = {}
    body = ""
    i = 1
    while i < len(lines) and lines[i].strip() != "":
        key, value = lines[i].split(": ")
        headers[key] = value
        i += 1
    if i + 1 < len(lines):
        body = "\n".join(lines[i + 1:])
    return {
        "status_code": status_code,
        "status_message": status_message,
        "headers": headers,
        "body": body
    }
