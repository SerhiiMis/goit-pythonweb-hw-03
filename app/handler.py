import mimetypes
import pathlib
import urllib.parse
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader
from .storage import load_data, save_message

class SimpleHandler(BaseHTTPRequestHandler):
    env = Environment(loader=FileSystemLoader("."))

    def do_POST(self):
        if self.path == '/message':
            data = self.rfile.read(int(self.headers['Content-Length']))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]} 

            save_message(
                username=data_dict.get("username", ""),
                message=data_dict.get("message", ""),
                timestamp=datetime.now().isoformat()
            )

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
        data = load_data()
        template = self.env.get_template("read.html")
        content = template.render(messages=data)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode("utf-8"))