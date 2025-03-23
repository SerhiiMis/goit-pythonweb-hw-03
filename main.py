import mimetypes
import pathlib
import urllib.parse
import json
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader

storage_dir = pathlib.Path("storage")
storage_dir.mkdir(exist_ok=True)

class SimpleHandler(BaseHTTPRequestHandler):
    env = Environment(loader=FileSystemLoader("."))

    def do_POST(self):
        if self.path == '/message':
            data = self.rfile.read(int(self.headers['Content-Length']))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

            file_path = storage_dir / "data.json"
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_data = {}

            existing_data[datetime.now().isoformat()] = {
                "username": data_dict.get("username", ""),
                "message": data_dict.get("message", "")
            }

            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(existing_data, f, ensure_ascii=False, indent=4)

            self.send_response(302)
            self.send_header('Location', '/')
            self.end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        if url.path == '/':
            self.send_html('index.html')
        elif url.path == '/message':
            self.send_html('message.html')
        elif url.path == '/read':
            self.render_read_page()
        elif pathlib.Path().joinpath(url.path[1:]).exists():
            self.send_static(url.path[1:])
        else:
            self.send_html('error.html', 404)

    def send_html(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as file:
            self.wfile.write(file.read())

    def send_static(self, filepath):
        self.send_response(200)
        mime_type, _ = mimetypes.guess_type(filepath)
        self.send_header('Content-type', mime_type or 'application/octet-stream')
        self.end_headers()
        with open(filepath, 'rb') as file:
            self.wfile.write(file.read())

    def render_read_page(self):
        file_path = storage_dir / "data.json"
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        template = self.env.get_template("read.html")
        content = template.render(messages=data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))


def run(server_class=HTTPServer, handler_class=SimpleHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    print("Server started at http://localhost:3000")
    http.serve_forever()


if __name__ == "__main__":
    run()
