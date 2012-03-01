# PennDOT Traffic Camera API

This simple API provides a way to query PennDOT traffic cameras
geographically.  To run the servers locally [mongoDB](http://www.mongodb.org/)
and [PyMongo](http://api.mongodb.org/python/current/) are required.  If they
are available, `run.py` will start them up and begin serving camera data
locally.

## First Time Startup

The first time that the servers are started up, they will perform a
`mongorestore` from the versioned mongoDB dump in the `data/dump/` directory.
This data will be restored to `data/db/` and `mongod` will use it as is
`dbpath`.

The `data/db/` is not versioned and contains relatively large working database
files.  The `.gitignore` specifies patterns to avoid committing changes to
those locations.
