import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from io import BytesIO

hostName = "localhost"
serverPort = 2104
passwords = {}


class MyServer(BaseHTTPRequestHandler):

    # health check
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = BytesIO()
        response.write("{\"status\": \"connected\"}".encode())
        self.wfile.write(response.getvalue())

    # get passwords
    def do_POST(self):
        global passwords
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode()

        self.send_response(200)
        self.end_headers()
        response = BytesIO()

        value = passwords.get(body)

        if value:
            response.write(str(value).encode())
        else:
            response.write("Password cannot be found".encode())

        self.wfile.write(response.getvalue())

    # update passwords
    def do_PUT(self):
        global passwords
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        body_string = body.decode()
        self.parsePasswords(json.loads(body_string))

        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        response = BytesIO()
        response.write("{\"status\": \"OK\"}".encode())
        self.wfile.write(response.getvalue())

    def parsePasswords(passwords_array):
        global passwords
        passwords = {}
        for elem in passwords_array:
            passwords[elem.get("title")] = elem.get("value")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
