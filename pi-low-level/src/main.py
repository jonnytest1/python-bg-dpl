
import traceback
import imp
import sys
import socketserver
import http.server
from customlogging import logKibana

sys.stdout = open("/home/jonathan/python/log.log", "a")

print("hello world")


class CustomHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.handleRequest("GET")

    def handleRequest(self, method):
        try:
            postdata = None
            if self.headers['Content-Length'] != None:
                postdata = self.rfile.read(
                    int(self.headers['Content-Length'])).decode('utf-8')

            response, mimetype = imp.load_source(
                "imports", "./imports.py").get_response(self, method, postdata)

            if(response is None):
                self.send_response(204)
                self.end_headers()
            else:
                self.send_response(200)
                self.send_header('Content-type', mimetype)
                self.end_headers()
                self.wfile.write(str.encode(response))
        except Exception as e:
            logKibana("ERROR", "error in requset", e)
            traceback.print_exc()

    def do_POST(self):
        self.handleRequest("POST")


PORT = 80
try:
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print("serving at port", PORT)
        try:
            httpd.serve_forever()
        except:
            print("clearing webserver")
            httpd.shutdown()
            httpd.socket.close()
except OSError as e:
    if e.strerror == "Address already in use":
        print("Address already in use")
    else:
        print(type(e).__name__)
        print(e)
