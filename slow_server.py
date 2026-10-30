import time
from http.server import BaseHTTPRequestHandler, HTTPServer


class SlowHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("Request received. Waiting 8 seconds...")

        time.sleep(8)

        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Slow test response")
        except BrokenPipeError:
            print("The client stopped waiting before the response was sent.")


server = HTTPServer(("127.0.0.1", 8000), SlowHandler)

print("Slow test server running at http://127.0.0.1:8000")

server.serve_forever()