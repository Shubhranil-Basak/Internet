from urllib.parse import urlparse, parse_qs

class Router:
    def __init__(self):
        self.routes = {"GET": {}, "POST": {}}

    def add_route(self, method, path, handler):
        self.routes[method][path] = handler

    def handle(self, method, path, body):
        parsed = urlparse(path)
        clean_path = parsed.path
        query_params = parse_qs(parsed.query)

        if clean_path in self.routes.get(method, {}):
            return self.routes[method][clean_path](body, query_params)
        else:
            return 404, "Not Found", {}, "Route not found"
