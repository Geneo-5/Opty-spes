import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import VERSION
import srv.service

try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    RESOURCE = os.path.abspath(os.path.join(getattr(sys, '_MEIPASS'),"clt/"))
except:
    RESOURCE = os.path.abspath(os.path.join(os.path.abspath(os.path.dirname(__file__)),"../clt/"))

MIMETYPE = {
    "html":'text/html',
    "css":'text/css',
    "csv":'text/csv',
    "jpg":'image/jpg',
    "png":'image/png',
    "js":'application/javascript',
    "map":'application/javascript',
    "json":'application/json',
}

class webServer(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"
        try:
            abspath = os.path.abspath(RESOURCE+self.path)
            if abspath.startswith(RESOURCE):
                mimetype = MIMETYPE[abspath.split(".")[-1]]
                self.send_response(200)
                self.send_header("Content-type", mimetype)
                self.end_headers()
                with open(abspath, "rb") as in_file:
                    tmp = in_file.read()
                    self.wfile.write(tmp.replace(b"###VERSION###", VERSION.VERSION.encode("utf8")))
            else:
                self.send_error(404,'File Not Found')
        except:
            self.send_error(404,'File Not Found, exception')

    def do_POST(self):
        try:
            if self.path in srv.service.SERVICE:
                # récupération des data
                length = int(self.headers['Content-Length'])
                if length > 10 * 1024 * 1024:
                    raise MemoryError("Out of memories")

                data = self.rfile.read(length)

                # éxécution du service
                message, typeData, autre = srv.service.SERVICE[self.path](data)

                if message == None:
                    self.send_response(200)
                    self.end_headers()
                    self.wfile.write(b'')
                    raise KeyboardInterrupt

                # envoie de la réponse
                self.send_response(200)
                self.send_header("Content-type", MIMETYPE[typeData])
                if autre:
                    for k in autre.keys():
                        self.send_header(k, autre[k])
                self.end_headers()
                self.wfile.write(message.encode('utf-8'))
            else:
                self.send_error(404,'File Not Found')
        except KeyboardInterrupt:
            sys.exit()

def start():
    print('Server listening on port 31415...')
    httpd = HTTPServer(('127.0.0.1', 31415), webServer)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")
    sys.exit()