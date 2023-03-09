# arctic

## Overview
Dashboard for ArcGIS Online/ArcGIS Portal.

This is a sandbox at the moment where I am testing out some ideas.

Today (29-Mar-22) I got an urge to try Webhooks so, see the README in the webhooks/ folder.
I think that it will end up being a microservice that catches events from Enterprise and publishes them via MQTT.
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

### FlexLM

I am now adding support for the ESRI LicenseManager (flexlm)
by merging in code from my previous docker project docker-flexlm.

The code for it is currently in mqtt_test because I am testing
using it to queue messages using MQTT. There is a client program
that subscribes to messages and a logwatch.py script that will
eventually watch the log file for FlexLM and publish changes to MQTT.

### MQTT

I am using MQTT for message queues so there is now a mqtt_broker
folder containing a set up for running Mosquitto in a Docker container.
It's very basic, included here for convenience; any MQTT broker should work.

It should be possible to install this project on different servers
so that you can test connections over the Internet.

It should be possible to put the MQTT broker behind a reverse proxy
so that it can be accessed securely over websockets.

### NPM and Node

The JavaScript portions of this project uses npm and the parcel bundler. Currently I do this by running the whole environment
in a docker container.

This saves me from having to install about 100 node packages
on the hosting server.

## Log files

Processing log files with ArcGIS Enterprise is problematic because the data are split between the web server (I'm using IIS for now),
Portal, Server, and Data Store.

If you want to trace an activity, for example who is using any given REST based service, then you can't just read one log file.
If the service is in Server, then you can find requests but they don't log the IP address of the requestor. The "web adaptor" blocks that.
They need some redesign here to fix this! 

Currently I am thinking about using one of those fancy logging tools that sucks the log files into a database. Apparently I have not
started making notes on this yet, so I think I will put more notes on this for now at this page: 
https://wiki.wildsong.biz/index.php?title=Arctic_Logging

### Cleaning

See [Clean](https://developers.arcgis.com/rest/enterprise-administration/enterprise/clean-logs.htm) for ?everywhere? and [Clean Logs](https://developers.arcgis.com/rest/enterprise-administration/server/cleanlogs.htm) for Server.

There is also a REST service [Clean Directory](https://developers.arcgis.com/rest/enterprise-administration/server/cleandirectory.htm)

I cannot find any way to clean the statistics folder. Mine has files going back to 2019.

### Web adaptors

Web Adaptors come first because these are the most useful logs.

Look for the config files to find the logs.
On IIS, mine were in C:/inetpub/logs/LogFiles/W3SVC

The config files are in an XML file C:/inetpub/wwwroot/{portal|server}/Web.config. Grep for log. There are settings here, for example when to role the files (weekly). The logfile location is in the  "customlocation" property.

***Both adaptors are set to log to the same file, how special!
I am inclined to fix that.***

### Portal logs
Can be queried via API. 

### Server logs

Can be queried via API. Find the config-store location via an API call, then look in the filesystem.

The file {config-store}/arcgis-logsettings.json has "logDir" set
to C:/arcgisserver/logs/ on my server. Other settings are in here
too, like the current logLevel and the number of days to keep logs.

There are separate logs for {serverfolder}/logs/{server|services|errorreports}/. "Errorreports" appears to be dumps that are only useful to forensic technicians at Esri. "Services" has a folder with logs for each running service.

A digression: [Work with server statistics](https://enterprise.arcgis.com/en/server/latest/administer/windows/working-with-server-statistics.htm)
There is something called **statisticsDir** in {directories}/arcgissystem. There is a 'statistics' folder there that has
many many files in it. Looks like one for every day the server has been in operation. Geez! Each one is a CSV with data on each
service. "Do not manually modify or delete files in this directory"
It says here ["Use ArcGIS Server Manager to access, view, configure, and delete reports"](https://enterprise.arcgis.com/en/server/latest/administer/windows/about-server-statistics.htm).

See [Usage Reports Configuration](https://delta.co.clatsop.or.us/server/admin/usagereports/settings). Default for "Keep statistics history" was forever. I changed it to 30 days. I don't see any way to clean up the 1650 extra files. I will leave it a few days, maybe
it will figure out they need to go tonight.

### Datastore logs

Strangely there are no entries in the REST viewer.
I could not see a way to query it in the API. Maybe there is none.

Server has an API call to find out what datastore is connected.
The file is in {config-store}/data/enterpriseDatabases/AGSDataStore*/dataItem.json

Datastore log files are in {arcgisdatastore}/logs/{MACHINE_FQDN}/{server|couchlog|database}

The **server** logs are the most interesting, they are either empty or full of dire messages about the status of validation check failures. I need to look at this.

The **database** logs include vacuum, postgres, and pg_dump entries. The postgresql files are moderately interesting. The pg_dump entries are all empty.

I have not looked at the **couchdb** logs yet but we don't 
do any scene / 3D stuff yet so they are probably empty.

### Resources

#### Esri

[Administering your GIS](https://developers.arcgis.com/python/guide/administering-your-gis/) Lots of interesting bits and bobs.

[Scripting ArcGIS Server administration](https://enterprise.arcgis.com/en/server/latest/develop/windows/scripting-arcgis-server-administration.htm)

#### Other

[OpenCV documentation](https://docs.opencv.org/4.2.0/)

[React Routing and Components for Signup and Login](https://saasitive.com/tutorial/react-routing-components-signup-login/)


[ArcGIS JavaScript API](https://developers.arcgis.com/javascript/latest/)  
[Portal access](https://developers.arcgis.com/javascript/latest/arcgis-organization-portals/) 

[ArcGIS REST API](https://developers.arcgis.com/rest/)  
[Web Map Specification](https://developers.arcgis.com/web-map-specification/)   
[load_web_map sample](https://developers.arcgis.com/javascript/latest/sample-code/webmap-basic/)  
[save_web_map sample](https://developers.arcgis.com/javascript/latest/sample-code/webmap-save/)  

