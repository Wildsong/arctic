# mqtt_broker

This is an MQTT broker that runs in a Docker container,
and implements both TCP and WebSockets interfaces.
If you use an nginx reverse proxy, it will run behind that.

## Configuration

Copy sample.env to .env and set it up for your network, this is mostly
for enabling the reverse proxy.

Mosquitto's config file is mosquitto.conf. It will be mounted when the
docker container starts. So edit and start (or restart) the container,
no need to copy it or install it anyplace.

Ports in use are 1883 and 9001.

* 1883 is for MQTT
* 9001 is for MQTT over WebSockets

## Launch

I often use docker-compose so I use "docker-compose up -d"
or with swarm it's "docker stack deploy -c docker-compose.yml mosquitto"

## Testing

You can use the command line to test pubish and subscribe as soon as the
broker container is running.

## Send a message (publish)

   docker exec -it mosquitto mosquitto_pub -t cc/flexlm -q 1 -d -m "`date +%H:%M:%S`"

where cc/flexlm is the topic and it sends a datetime stamp as the payload.

## Receive messages (subscribe)

   docker exec -it mosquitto mosquitto_sub -t cc/# -q 1 -d

where it subscribes to all topics starting with cc/ and prints incoming
messages to the screen.

## Resources

https://hub.docker.com/_/eclipse-mosquitto

