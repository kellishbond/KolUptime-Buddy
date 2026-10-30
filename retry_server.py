import time
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

request_count = 0
lock = threading.Lock()


class RetryHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global request_count

        with lock:
            request_count += 1
            current_request = request_count

        print(f"Received request number {current_request}")

        if current_request == 1:
            print("First request: Delaying response for 8 seconds...")
            time.sleep(8)

        try:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Website is working!")
        except BrokenPipeError:
            print("Client stopped waiting for this request.")


server = ThreadingHTTPServer(("127.0.0.1", 8000), RetryHandler)

print("Retry test server running at http://127.0.0.1:8000")

server.serve_forever()