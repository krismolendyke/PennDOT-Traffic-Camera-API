#!/usr/bin/env python

"""Query for PennDOT traffic cameras in District 6."""

from bson.son import SON
from pprint import pprint as pp
from pymongo import Connection
import argparse
import json
import sys

class PennDOTCameras(object):
    """Get information about PennDOT District 6 cameras."""

    DATABASE = "penndotcameras"
    DISTRICT_6 = "district6"
    R = 6378 # Radius of Earth in kilometers
    KM_PER_MI = 0.6378 # Kilometers per mile

    def __init__(self, host="localhost", port=27017):
        super(PennDOTCameras, self).__init__()
        self.connection = Connection(host, port)
        self.db = self.connection[PennDOTCameras.DATABASE]
        self.d6 = self.db[PennDOTCameras.DISTRICT_6]

    def getCamerasNear(self, lat, lng, num=2):
        query = SON([("geoNear", PennDOTCameras.DISTRICT_6),
                     ("near", [lat, lng]),
                     ("num", num),
                     ("spherical", True)])
        cameras = self.db.command(query)["results"]
        for camera in cameras:
            for key, val in camera["obj"].items():
                if key != "_id":
                    camera[key] = val
            camera.pop("obj", None)
            camera[u"miles_away"] = round(camera["dis"] * PennDOTCameras.R *
                                          PennDOTCameras.KM_PER_MI, 2)
            camera.pop("dis", None)
        return cameras

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__.strip(),
                                     epilog="So it goes.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", default=27017)
    args = parser.parse_args()
    pdc = PennDOTCameras(args.host, args.port)
    cameras = pdc.getCamerasNear(39.875833, -75.348917, 5)
    print json.dumps(cameras)
