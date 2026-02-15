"""Local dev server - replaces 'vercel dev' for local testing"""

import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from dotenv import load_dotenv

load_dotenv()

from chat_core import get_chat_response


class DevHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory="public", **kwargs)

    def do_POST(self):
        if self.path != "/api/chat":
            self.send_error(404)
            return

        try:
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))

            question = data.get('question', '')
            chat_history = data.get('chat_history', [])

            result = get_chat_response(question, chat_history)
            self._send_json(200, result)

        except Exception as e:
            print(f"Error: {e}")
            self._send_json(500, {"error": str(e)})

    def _send_json(self, code, data):
        self.send_response(code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == "__main__":
    server = HTTPServer(('localhost', 3000), DevHandler)
    print("Dev server running at http://localhost:3000")
    server.serve_forever()
