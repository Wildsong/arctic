class Config(object):
    MQTT_BROKER="192.168.123.2"
    MQTT_PORT=9001
    MQTT_KEEPALIVE=60
    MQTT_TRANSPORT="websockets"

    TOPIC_TEXT = 'cc/flexlm'
    TOPIC_ALERT = 'cc/push'
    TOPIC_IMAGE = 'cc/image'


