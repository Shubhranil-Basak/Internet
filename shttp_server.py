from shttp.server.router import Router
from shttp.server.core import SHTTPServer

router = Router()

def hello_handler(body, query):
    print("Query parameters:", query)
    name = query.get("name", ["Guest"])[0]
    age = query.get("age", ["unknown"])[0]
    text = f"Hello {name}, you are {age} years old!"
    return 200, "OK", {"Content-Type": "text/plain"}, text


def greet_handler(body, query):
    return 200, "OK", {"Content-Type": "text/plain"}, f"Hello from POST! You sent: {body}"


router.add_route("GET", "/hello", hello_handler)
router.add_route("POST", "/greet", greet_handler)

server = SHTTPServer("localhost", 8081, router)
server.start()
