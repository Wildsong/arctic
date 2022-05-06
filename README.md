# arctic

## Overview
Dashboard for ArcGIS Online/ArcGIS Portal.

This is a sandbox at the moment where I am testing out some ideas.

Today (29-Mar-22) I got an urge to try Webhooks so, see the README in the webhooks/ folder.
I think that it will end up being a microservice that catches events from
Enterprise and publishes them via MQTT.
Hence the mqtt_broker/ and mqtt_test/ folders, which I have not look at for a few months.

For Prometheus + Grafana in Docker, 
see the README in the prometheus/ folder.

## Set up

### Conda environment for Python packages

```bash
On Windows, use the old Python to avoid DLL errors.
    conda create --name=arctic --file=requirements.txt -c conda-forge python=3.7.9

On Linux, 
    conda create --name=arctic --file=requirements.txt -c conda-forge 

conda activate arctic
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

[OpenCV documentation](https://docs.opencv.org/4.2.0/)

[React Routing and Components for Signup and Login](https://saasitive.com/tutorial/react-routing-components-signup-login/)

