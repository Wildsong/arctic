# arctic

## Overview
Dashboard for ArcGIS Online/ArcGIS Portal.

This is totally just a dev project at the moment where I am
testing out ideas.

At the moment I am looking at Prometheus + Grafana in Docker.
See the README in the prometheus/ folder.

## Set up

### Conda environment for Python packages

When running on a system with ArcGIS Pro installed,
VS Code is happier if you clone the ESRI environment.
You will get DLL errors and complaints about pandas if you don't

```bash
    # If you have Pro installled
    conda create --name=arctic --clone=arcgispro-py3
    # If you don't
    conda create --name=arctic
    # Either way, activate the environment and add the rest
    conda activate arctic
    conda install --file=requirements.txt
```

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

## Node

** This project currently does NOT use NPM. ** I am not working on that
part right now.

The project uses npm and the parcel bundler. You need to install npm and then
install parcel globally. (``npm install parcel -g``) Once you have done that, use
```
npm start
```
to launch node and open a brower on http://localhost:1234/

### Resources

[OpenCV documentation (https://docs.opencv.org/4.2.0/)]


