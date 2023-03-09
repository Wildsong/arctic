# geodatabase

This is an api that returns information about an Esri geodatabase server.

Currently it just returns a table about compressions.

## The obligatory screenshot

![Screenshot](screenshot.png?raw=true "What the web page looks like")

### Prerequisites

### Docker build

Because of the licensing constraints I don't push any image file up to Docker Hub.

Make sure you've downloaded the tar.gz file, see Prerequisites.

Then run the build command to create images for the license manager and the monitor.

```bash
docker compose build
```

## Deployment

You just have to run the container. Docker-compose.yml has the 
environment set up and is set to restart so use that.

```bash
docker compose up -d
```
