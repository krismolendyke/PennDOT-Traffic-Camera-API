#!/usr/bin/env python

"""A simple HTTP server for PennDOT camera data."""

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from penndotcameras import PennDOTCameras
from pprint import pprint as pp
import json
import urlparse

class RequestHandler(BaseHTTPRequestHandler):
    """Handle GET requests for PennDOT traffic cameras."""

    def do_GET(self):
        """Get JSON/P describing cameras near a given location.

        The request URL path must be of the form:

            /lat/lng/num

        Where lat and lng are valid floats and num is a valid int.  If that is
        the case, a list of cameras sorted by ascending distance from the
        given location, of a maximum length of num, will be returned as JSON.

        If the request URL is specified with a query string parameter of:

            callback=callbackFunctionName

        The response will be returned as JSONP using callbackFunctionName.
        """
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
            num = int(path[2])
        except Exception:
            self.send_response(400)
            self.end_headers()
            self.wfile.write("Latitude, longitude and number of cameras must "
                             "be numbers specified in the request URL path "
                             "as '/lat/lng/num'.")
            return

        pdc = PennDOTCameras()
        response = json.dumps(pdc.getCamerasNear(lat, lng, num),
                              separators=(',',':'))

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
