# flexlm

2024-04-11 Added Windows support so that I can tail the debug log file.
2024-04-10 Updated for 2023 FlexLM and switched from CentOS 7 to Rocky Linux 9 in build stage.
2023-03-10 Converted from waitress to bjoern  
2023-03-09 This used to be a separate project called "arctic-monitor", today I rolled it into Arctic

* I tried running this container on Windows Desktop (in a Linux docker) and it could not connect to the real license server. Whatever. Weird use case anyway.

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

### Next Generation version

The advantage of watching the log instead of polling lmutil
is that the monitor can respond as soon as anything happens instead of at polling intervals.
The disadvantage is it precludes multiple redundant license servers but no one seems
to do that with ArcGIS anyway.

If I put a microservice on the actual license manager, and let it run both lmstat
and monitor the logs, it could run lmstat directly from Windows. But ugh. Windows.
So for now I will just try to bind mount the log directory and then tail it from
the Docker container.

The microservice will be a GraphQL publisher.

Okay, so I have to rewrite everything to run directly in Docker, not Docker Compose, because I don't have Docker Compose installed on Windows Server.

TODO

Write the front end. When it starts, it will subscribe to notifications from the server.

In the server, poll the output from lmstat.bat periodically. Push updates to the front end.
Read the log file, parse it and collect current status, then as it changes, push notifications to the front end.

## The obligatory screenshot

![Screenshot of monitor for ArcGIS Flexlm](screenshot.png?raw=true "What the web page looks like")

### Prerequisites

#### Linux only

Dockerfile.linux is based on the 2023.0 version of the license manager.
If you are building the Windows version there is no need to download anything.

I don't think it matters very much which version you use, because it is
just interrogating the real license server over a network connection.
But when the version number changes you can change the Dockerfile.

To get the tar file, go to my.esri.com and download the latest Linux
license manager.  It will be a file ending in 'tar.gz'. Put the file
in this folder. (The one containing the Dockerfiles.)

#### License file (all versions)

You  have to put a copy of your service.txt file
from your license server here so that it can be baked into the build. 
The original is with the license manager, on Windows it's in
C:\Program Files\ArcGIS\LicenseManager\bin.

You need to **edit the service.txt** file so that it has the actual license server
host name instead of "This_Host".  Copy the service.txt file into the
config/ directory, and edit it. In my case I put the full name in there
including the domain, else Docker wanted to use a "hostname.local" address
that resolved to an IPV6 address that we don't support.

When you don't set the host name successfully, you will get a socket error because lmutil
defaults to using a socket connection instead of a network connection.

### Build image

#### Dockerfile

This version builds on a Windows server so that the log file can be accessed.
(Assuming you run your FlexLM on Windows not Linux.)

Build the image.

   docker build -t lmstat .

#### Dockerfile.linux

NOTE I stopped working on this one when I started on the Windows version.

This version builds with the tarfile because it does not have to run on the license manager host.
Because of the licensing constraints I don't push any image file up to Docker Hub.
Make sure you've downloaded the tar.gz file, see Prerequisites.

The requirements doc at ESRI call for RHEL 8 or 9;
this Dockerfile uses Rocky Linux 9 and Debian 11.

The license manager installation step is done in "silent" mode so
there is no requirement for any X Window server or any interactions
from you. 

I don't like Redhat, so stage 2 of the Dockerfile uses Debian.
The final image is smaller. I am sure it could go a lot smaller but
I am done for today. Maybe someone could make it run in Alpine?

If the build fails with a message about not being able to ADD then you
did not put the tar.gz file here or you need to update its name in
"Dockerfile" around line 40.

After the license manager is installed Docker will emit a long series
of Copy File and Install File messages from the flexlm installer. It
will stop at this point if the install fails.

Build the image.

   docker build -t lmstat .

The only file we need from the ESRI installation is lmutil.
When the stage 2 image is built, the file will be copied from the stage1 image to the stage 2.
(All that work it does just for one file!!)

Once the builds complete you will have an image
containing the lmutil tool and the python web server.

### Confirm the build (optional step!)

You can look around in the new container by launching into a bash shell.
If you don't want to, skip to the next section.

#### Talking to the license manager

   bin="C:\\Program Files\\ArcGIS\\LicenseManager\\bin"
   dstbin="C:\\srv\\bin"
   docker container run --rm -it -v "$src:$dst" lmstat

When you are in the shell you can run "lmstat" and it should dump
out the license info. 

#### WATCHING THE LOG FILE

Where are the log files? Here: C:/ProgramData/ArcGIS/LicenseManager
(The debug log file is lmgrd9.log; the other files in that folder are not useful.)

I can connect and dump out the contents of the file,

   logs="C:\\ProgramData\\ArcGIS\\LicenseManager"
   dstlogs="C:\srv\logs"
   docker container run --rm -it -v "$logs:$dstlogs" lmstat
   type logs\lmgrd9.log

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

Since I can watch the file, I can build this application. **:-) YAY.**

## Deployment

You just have to run the container. In the Linux world this starts a web server.

   docker compose up -d

Everything changed in Windows world and this will not work.

    docker run -d -e LICENSE=/srv/arctic/service.txt -e MODULE_NAME=app.start_server -p 5500:80 lmstat

## Misc additional notes

### Another similar project

Uses lmutil and stores output in SQL Server:
<https://github.com/jmitz/ArcGISLicenseMonitor/blob/master/LicenseMonitor.py>

### "REPORT" LOGGING - can be enabled in OPTIONS file but produces an encrypted file that is of no use without Flexera software

See <https://openlm.com/blog/are-flexnet-flexlm-manager-report-logs-essential-for-license-consumption-monitoring/>

## Resources

https://blog.theodo.com/2018/02/real-time-notification-system-graphql-react-apollo/

