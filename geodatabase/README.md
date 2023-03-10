# geodatabase_api

This is an api that returns information about an Esri geodatabase server.

Currently it just returns a table about compressions.

## The obligatory screenshot

Nah not yet
![Screenshot](screenshot.png?raw=true "What the web page looks like")

### Prerequisites

Copy sample.env to .env and edit as needed for your environment.

### Docker build

Run the build command to create image for the service.

```bash
# faster
docker buildx build -t arctic-geodatabase-api .

# slower but easier to type
docker compose build
```

## Deployment

You just have to run the container. Docker-compose.yml has the 
environment set up and is set to restart so use that.

```bash
docker compose up -d
```
