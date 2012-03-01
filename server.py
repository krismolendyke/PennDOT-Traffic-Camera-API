#!/usr/bin/env python

"""Simple server for PennDOT camera data."""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from penndotcameras import PennDOTCameras
from pprint import pprint as pp
import json
import urlparse

class RequestHandler(BaseHTTPRequestHandler):
    """docstring for RequestHandler"""

    def do_GET(self):
        split_path = urlparse.urlsplit(self.path)
        path = split_path.path.split("/")[1:]

        if len(path) < 3:
            self.send_response(404)
            self.end_headers()
            self.wfile.write("Not Found.")
            return

        try:
            lat = float(path[0])
            lng = float(path[1])
            num = float(path[2])
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Latitude, longitude and number of cameras must "
                             "be numbers specified in the request URL path "
                             "as '/lat/lng/num'.")
            return

        pdc = PennDOTCameras()
        response = json.dumps(pdc.getCamerasNear(lat, lng, num))

        query = urlparse.parse_qs(split_path.query)
        if "callback" in query:
            response = "%s(%s)" % (query["callback"][0], response)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(response)
        return

if __name__ == "__main__":
    server = HTTPServer(("localhost", 1776), RequestHandler)
    server.serve_forever()
