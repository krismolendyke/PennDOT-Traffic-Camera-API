#!/bin/sh/env python

"""Run all of the servers required to use PennDOT cameras locally.

If this script succeeds, visiting http://localhost:1776/lat/lng/num will
return JSON describing a list of PennDOT cameras.  Cameras are returned in
order of increasing distance from the given lat/lng. num is the number of
cameras nearest the given location that you would like returned.

Visiting http://localhost:8000 will display a simple webpage which consumes
that JSON and displays PennDOT cameras nearest to your current location.
"""

from SimpleHTTPServer import SimpleHTTPRequestHandler
import os
import SocketServer
import subprocess

def print_box(text):
    """
    1. Create a box.
    2. Put your text in that box.
    3. Make her read the box.
    """
    print "#" * 78
    print "#%s#" % (" " * 76)
    for line in text.splitlines():
        print "# %s #" % line.rstrip().ljust(74, " ")
    print "#%s#" % (" " * 76)
    print "#" * 78

if __name__ == "__main__":
    db_path = os.path.join(os.getcwd(), "data", "db")

    if not os.path.exists(db_path):
        dump_path = os.path.join(os.getcwd(), "data", "dump")
        print_box("""No mongoDB database path is available.

One will be created for you now from the versioned data dump at:

%s""" % dump_path)
        os.makedirs(db_path)
        subprocess.call(["mongorestore", "--dbpath", db_path, dump_path])

    mongod = subprocess.Popen(["mongod", "--dbpath", db_path])
    server = subprocess.Popen(["./server.py"])
    httpd = SocketServer.TCPServer(("", 8000), SimpleHTTPRequestHandler)
    if mongod.returncode is None and server.returncode is None:
        print_box("""Servers are up and running!  Visit the follow URLs to see them in action:

    http://localhost:8000
    http://localhost:1776/39.875833/-75.348917/2
""")
        httpd.serve_forever()
