def parse_request(data):
    lines = data.strip().split("\n")
    method, path = lines[0].split()
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
        "method": method,
        "path": path,
        "headers": headers,
        "body": body
    }

def build_response(status_code, status_message, headers=None, body=""):
    headers = headers or {}
    headers["Content-Length"] = str(len(body))
    header_lines = [f"{k}: {v}" for k, v in headers.items()]
    return f"{status_code} {status_message}\n" + "\n".join(header_lines) + "\n\n" + body
