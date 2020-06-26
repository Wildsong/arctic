import paho.mqtt.client as mqttClient
from config import Config
import io
import cv2

def on_connect(client, userdata, flags, rc):
    result = mqttClient.connack_string()
    print("on_connect", result)

def on_receive(client, userdata, msg):
    if msg.topic == Config.TOPIC_IMAGE:
        print(msg.topic, "payload: IMAGE")
        jpeg = io.BytesIO(msg.payload)
        result, image = cv2.imdecode(jpeg)
        cv2.imshow("mqttClient", image)
    else:
        print(msg.topic, "payload \"%s\"" % msg.payload.decode('utf-8'))


cv2.namedWindow("mqttClient")

client = mqttClient.Client(client_id='reader', transport=Config.MQTT_TRANSPORT, clean_session=True)
client.on_connect = on_connect
client.on_message = on_receive
client.connect(Config.MQTT_BROKER, Config.MQTT_PORT, 60)
client.subscribe(Config.TOPIC_TEXT)
client.subscribe(Config.TOPIC_IMAGE)
client.subscribe(Config.TOPIC_ALERT)
client.loop_forever()
