# A stand-in for the app containers in nginx.sh: answers every GET with its own name and the
# path it received, so the log shows what nginx forwarded. Not the tutorial's code.
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer

NAME, PORT = sys.argv[1], int(sys.argv[2])

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = json.dumps({"container": NAME, "path_seen": self.path}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body + b"\n")
    def log_message(self, *a):
        pass

HTTPServer(("0.0.0.0", PORT), H).serve_forever()
