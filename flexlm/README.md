# flexlm

2024-04-10 Updated for 2023 FlexLM and switched from CentOS 7 to Rocky Linux 9 in build stage.
2023-03-10 Converted from waitress to bjoern  
2023-03-09 This used to be a separate project called "arctic-monitor", today I rolled it into Arctic


* I tried running this container on Windows Desktop (in a Linux docker) and it could not connect to the real license server. Whatever. Weird use case anyway.
* I tried to use Debian 11 in stage 2 and failed. Sticking with Centos.
* I updated it to run the 2022 license manager. That worked. Finally something worked.

2022-06 I am working on turning this into a microservice instead of a full web page,
so the web page you can load at port 5000 is no longer as pretty as it used to be.
(See the notes on version 2 all the way at the bottom of this page.)
I got arctic-monitor to a useful stage and now I work on it when time permits.

System for monitoring an ArcGIS concurrent license manager

This is a small Dockerized app written in Python running as a service.
The Python script needs to query the license manager and it does that
using the "lmutil" command line utility that is included in the
Esri download for the license manager.

Because the license manager "Flexera FlexLM" is licensed software, if
you want to use this monitor in the Docker, you will need to download
the Linux version of the license manager package from ESRI and put it
here in the project folder before doing the Docker build.

## The obligatory screenshot

![Screenshot of monitor for ArcGIS Flexlm](screenshot.png?raw=true "What the web page looks like")

### Prerequisites

The Dockerfile is based on the 2023.0 version of the license manager.

I don't think it matters very much which version you use, because it is
just interrogating the real license server over a network connection.
But when the version number changes you can change the Dockerfile.

To get the tar file, go to my.esri.com and download the latest Linux
license manager.  It will be a file ending in 'tar.gz'. Put the file
in this folder. (The one containing the Dockerfiles.)

### Notes on the Dockerfile

The requirements doc at ESRI call for RHEL 8 or 9;
this Dockerfile uses Rocky Linux 9 and Debian 11.

The license manager installation step is done in "silent" mode so
there is no requirement for any X Window server or any interactions
from you.

I don't like Redhat, so stage 2 of the Dockerfile uses Debian.
The final image is smaller. I am sure it could go a lot smaller but
I am done for today. Maybe someone could make it run in Alpine?

### Docker build

Because of the licensing constraints I don't push any image file up to Docker Hub.

Make sure you've downloaded the tar.gz file, see Prerequisites.

Then run the build command to create images for the license manager and the monitor.

**Install service.txt** -- In the interest of simplicity you 
have to put a copy of your service.txt file
from your license server here so that it can be baked into the build. 
You need to edit the service.txt file so that it has the actual license server
host name instead of "This_Host".  Copy the service.txt file into the
config/ directory, and edit it.

Build the image.

   docker compose build

If the build fails with a message about not being able to ADD then you
did not put the tar.gz file here or you need to update its name in
"Dockerfile" around line 40.

After the license manager is installed Docker will emit a long series
of Copy File and Install File messages from the flexlm installer. It
will stop at this point if the install fails.

For the monitor, the only file we need from the ESRI installation is lmutil.
When the stage 2 image is built, the file will be copied from the stage1 image to the stage 2.

Once the builds complete you will have an image
containing the lmutil tool and the python web server.

### Confirm the build (optional step!)

You can look around in the new container by launching into a bash shell.
If you don't want to, skip to the next section.

   docker run -it --rm arctic-flexlm-monitor bash

When you are in the shell you can run "lmstat -a" and it should dump
out the license info. You can run "python /app/app/lmutil.py" to make sure
it can run the Python as well.

## Deployment

You just have to run the container. Docker-compose.yml has the
environment set up and is set to restart so use that.

   docker-compose up -d

## Misc additional notes

I previously started working on a Windows-based monitor and quit when
I found out how hard it was (FOR ME) to work with Docker On Windows.

### Another similar project

Uses lmutil and stores output in SQL Server:
<https://github.com/jmitz/ArcGISLicenseMonitor/blob/master/LicenseMonitor.py>

### WATCHING THE LOG FILE

Where are the log files?

   C:/ProgramData/ArcGIS/LicenseManager/lmgrd9.log

```bash
13:01:46 (lmgrd) -----------------------------------------------
13:01:46 (lmgrd)   Please Note:
13:01:46 (lmgrd)
13:01:46 (lmgrd)   This log is intended for debug purposes only.
13:01:46 (lmgrd)   In order to capture accurate license
13:01:46 (lmgrd)   usage data into an organized repository,
13:01:46 (lmgrd)   please enable report logging. Use Flexera's
13:01:46 (lmgrd)   software license administration  solution,
13:01:46 (lmgrd)   FlexNet Manager, to  readily gain visibility
13:01:46 (lmgrd)   into license usage data and to create
13:01:46 (lmgrd)   insightful reports on critical information like
13:01:46 (lmgrd)   license availability and usage. FlexNet Manager
13:01:46 (lmgrd)   can be fully automated to run these reports on
13:01:46 (lmgrd)   schedule and can be used to track license
13:01:46 (lmgrd)   servers and usage across a heterogeneous
13:01:46 (lmgrd)   network of servers including Windows NT, Linux
13:01:46 (lmgrd)   and UNIX.
13:01:46 (lmgrd)
13:01:46 (lmgrd) -----------------------------------------------
13:01:46 (lmgrd)
13:01:46 (lmgrd)
13:01:46 (lmgrd) Server's System Date and Time: Sun Mar 17 2024 13:01:46 Pacific Daylight Time
13:01:46 (lmgrd) pid 6676
.
.
.
14:46:39 (telelogic) DENIED: DOORS indkach@indkach  [telelogic]
(Licensed number of users already reached. (-4,342:10054 ))
14:46:39 (telelogic) DENIED: DOORS indkach@indkach  [telelogic]
(Licensed number of users already reached. (-4,342:10054 ))
14:46:39 (telelogic) OUT: TLSTOK-token indkach@indkach  [DOORS]
(3 licenses)
```

### "REPORT" LOGGING - can be enabled in OPTIONS file but produces an encrypted file that is of no use without Flexera software

See <https://openlm.com/blog/are-flexnet-flexlm-manager-report-logs-essential-for-license-consumption-monitoring/>

### Version 2 ideas

The advantage of watching the log instead of polling lmutil
is that the monitor can respond as soon as anything happens instead of at polling intervals.
The disadvantage is it precludes multiple redundant license servers but no one seems
to do that with ArcGIS anyway.

If I put a microservice on the actual license manager, and let it run both lmstat
and monitor the logs, it could run lmstat directly from Windows. But ugh. Windows.
So for now I will just try to bind mount the log directory and then tail it from
the Docker container.

The microservice will be a GraphQL publisher.
