# arctic

## Overview
Dashboard for ArcGIS Online/ArcGIS Portal.

This is a sandbox at the moment where I am testing out some ideas.
So far all I have here is an attempt at gathering data and graphing.

Today (29-Mar-22) I got an urge to try Webhooks so, see the README in the webhooks/ folder.
I think that it will end up being a microservice that catches events from
Enterprise and publishes them via MQTT.
Hence the mqtt_broker/ and mqtt_test/ folders, which I have not look at for a few months.

For Prometheus + Grafana in Docker, 
see the README in the prometheus/ folder.

## Set up


## FlexLM

I am now adding support for the ESRI LicenseManager (flexlm)
by merging in code from my previous docker project docker-flexlm.

The code for it is currently in mqtt_test because I am testing
using it to queue messages using MQTT. There is a client program
that subscribes to messages and a logwatch.py script that will
eventually watch the log file for FlexLM and publish changes to MQTT.

## MQTT

I am using MQTT for message queues so there is now a mqtt_broker
folder containing a set up for running Mosquitto in a Docker container.
It's very basic, included here for convenience; any MQTT broker should work.

It should be possible to install this project on different servers
so that you can test connections over the Internet.

It should be possible to put the MQTT broker behind a reverse proxy
so that it can be accessed securely over websockets.

## GraphQL

MQTT is nifty for IoT but GraphQL makes more sense for this project.

## Python for the API (server) side

I am using the Apollo client and wondering if
I can still use Apollo with a Python backend?

Of COURSE!

https://strawberry.rocks/

https://www.apollographql.com/blog/backend/federation/add-python-to-your-graphql-api-with-graphos-and-strawberry-graphql?referrer=python-strawberry-subgraph

https://www.apollographql.com/blog/graphql/python/complete-api-guide/

### Conda environment for Python packages

2023-07-04 Current version of arcgis is 2.1.0.3

```bash

2023-07-04 update -- still ?? maybe this was fixed in arcgis-2.x ? Trying it.
My notes say, "On Windows, use the old Python to avoid DLL errors."

    conda create --name=arctic --file=requirements.txt -c conda-forge -c esri python=3.7.9

On Linux, 

    conda create --name=arctic --file=requirements.txt -c conda-forge -c esri

And then on either platform, install all required packages and start a GraphQL server.

    cd server
    conda activate arctic
    pip install 'strawberry-graphql[debug-server]'
    pip innstall rich
    strawberry server schema

Runs a test server on port 8000. Connect via browser and send it a ping, like this.

    {
        ping {
            timestamp
        }
    }

It should respond with something like this.

    {
        "data": {
            "ping": {
            "timestamp": "2023-07-05T15:02:59.334306"
            }
        }
    }

Ask it for some licenses, like this

    {
        licenses {
            id
            product
        }
    }

I am thinking I actually will end up needing several GraphQL servers,
one for ArcGIS, one for the FlexLM license manager. Maybe one for MapProxy.
There's also Prometheus, that might be enough for MapProxy.

Now that a service is running, run the front end to talk to it.

## Node on the client (browser) side

The project uses npm. You need to install npm.

    cd client
    npm install
    npm start

to launch node and open a browser

## Licenses

Displays information on licenses from FlexLM in a 
[react-date-grid](https://www.npmjs.com/package/react-data-grid).

### Resources

[OpenCV documentation](https://docs.opencv.org/4.2.0/)


