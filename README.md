# PennDOT Traffic Camera API

This simple API provides a way to query PennDOT traffic cameras
geographically.

## Requirements

1. [mongoDB](http://www.mongodb.org/)
1. [PyMongo](http://api.mongodb.org/python/current/)

## Running Locally

`python run.py` will start all of the servers required for testing or
developing on a local machine.

Visiting http://localhost:8000 will display a very simple web page which
consumes the API and displays PennDOT traffic cameras near your current
location.

### Local Servers

There are three server components that will be started:

1. A `mongod` server pointed at local PennDOT traffic camera data.
1. A `server.py` HTTP server which responds to specific `GET` requests with PennDOT camera JSON/P.
1. A `python -m SimpleHTTPServer` HTTP server serving files out of the current directory.

### A Note Regarding First Time Startup

The first time that the servers are started up, they will perform a
`mongorestore` from the versioned mongoDB dump in the `data/dump/` directory.
This data will be restored to `data/db/` and `mongod` will use it as is
`dbpath`.

The `data/db/` is not versioned and contains relatively large working database
files.  The `.gitignore` specifies patterns to avoid committing changes to
those locations.

## Using the API

A `GET` request made to `http://localhost:1776/lat/lng/num` will return
traffic camera JSON.  This URL path has the following requirements to return
valid traffic camera data:

* `lat` must be a `float` parseable latitude value
* `lng` must be a `float` parseable longitude value
* `num` must be an `int` parseable number of camera data items to return value

For example, requesting `http://localhost:1776/39.875833/-75.348917/2` will
return:

```javascript
[{"loc":{"y":39.875833,"x":-75.348917},"name":"I-476 McDade on Ramp","url":"http://www.dot35.state.pa.us/public/Districts/District6/WebCams/D6Cam122.jpg","miles_away":0.0,"roadId":"i476","road":"Interstate 476"},{"loc":{"y":39.876783,"x":-75.35165},"name":"I-476 SB @ Mcdade Blvd/Exit 1","url":"http://www.dot35.state.pa.us/public/Districts/District6/WebCams/D6Cam123.jpg","miles_away":0.19,"roadId":"i476","road":"Interstate 476"}]
```

Pretty printed:

```javascript
[
    {
        "loc": {
            "x": -75.348917,
            "y": 39.875833
        },
        "miles_away": 0.0,
        "name": "I-476 McDade on Ramp",
        "road": "Interstate 476",
        "roadId": "i476",
        "url": "http://www.dot35.state.pa.us/public/Districts/District6/WebCams/D6Cam122.jpg"
    },
    {
        "loc": {
            "x": -75.351650000000006,
            "y": 39.876783000000003
        },
        "miles_away": 0.19,
        "name": "I-476 SB @ Mcdade Blvd/Exit 1",
        "road": "Interstate 476",
        "roadId": "i476",
        "url": "http://www.dot35.state.pa.us/public/Districts/District6/WebCams/D6Cam123.jpg"
    }
]
```
