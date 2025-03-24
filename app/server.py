from http.server import HTTPServer
from .handler import SimpleHandler

def run_server(port=3000):
    server_address = ('', port)
    http = HTTPServer(server_address, SimpleHandler)
    print(f"Server started at http://localhost:{port}")
    http.serve_forever()