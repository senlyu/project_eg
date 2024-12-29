from http.server import BaseHTTPRequestHandler, HTTPServer

test = "123"

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Log the request path
        print(f"Received GET request for: {self.path}")
        
        # Respond with a basic HTML message
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(bytes(f"<html><body><h1>Hello, World! {test} </h1></body></html>", "utf-8"))

# Set up the HTTP server
host = "localhost"
port = 8001
server = HTTPServer((host, port), MyHandler)
print(f"Custom server running at http://{host}:{port}")
server.serve_forever()