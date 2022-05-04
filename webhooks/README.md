# webhooks

This is a flask app that provides a webhooks microservice
for the Arctic project.

## Set up

I worked on having this run on the local machine for debugging
and gave up on that because I needed to go to a real service.
When you set a webhook in Portal, it has to point at a real URL,
not a port forwarded one.

I have pushed the image for wildsong/flask to hub.docker.com but 
if you want to create a basic flask docker yourself, 
use the https://github.com/wildsong/flask_template project.

project_requirements.txt currently has a few packages that I am
not using here yet but anticipate needing any day now, including
pandas and sqlalchemy.

## Running in Docker for testing

```bash
docker-compose build
docker-compose up -d
```
