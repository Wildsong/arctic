# Watch log files for specific events and publish them
#
import os
import paho.mqtt.publish as publish
import re
from datetime import datetime
from time import sleep
import cv2
from config import Config

# TIME (VENDOR) (SUMMARY)|EVENT:
TIMESTAMP = 1
EVENT = 2
DATA = 3
re_IN = re.compile(r'^([\d\:]+) \(\w+\) (IN): (.*)')
re_OUT = re.compile(r'^([\d\:]+) \(\w+\) (OUT): (.*)')
re_DENIED = re.compile(r'^([\d\:]+) \(\w+\) (DENIED): (.*)')
re_UNSUPPORTED = re.compile(r'^([\d\:]+) \(\w+\) (UNSUPPORTED): (.*)')

DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"

imagefile = "./assets/Capture.png"
def load_image():
    image = None
    with open(imagefile, "rb") as fp:
        image = fp.read()
    return image

def parse_log(entry):
    """ Returns a tuple containing 2 strings: event, timestamp+information. """

    #print(entry)
    # INFO
    mo = re_IN.search(entry)
    if mo:
        return (INFO, mo.group(TIMESTAMP) + ' ' + mo.group(DATA))
    mo = re_OUT.search(entry)
    if mo:
        return (INFO, mo.group(TIMESTAMP) + ' ' + mo.group(DATA))

    # WARNING
    mo = re_UNSUPPORTED.search(entry)
    if mo:
        return (WARNING, mo.group(TIMESTAMP) + ' ' + mo.group(DATA))

    # ERROR
    mo = re_DENIED.search(entry)
    if mo:
        return (ERROR, mo.group(TIMESTAMP) + ' ' + mo.group(DATA))

    # Meaningless log entry
    return (None, None)

def on_connect(client, userdata, flags, rc):
    #result = mqttClient.connack_string()
    print("on_connect", rc)

def on_publish(client, userdata, mid):
    print("published")

logfile = 'sample.log'

#mqttClient = mqtt.Client(client_id="flex")
#mqttClient.on_connect = on_connect
#mqttClient.on_publish = on_publish
#mqttClient.connect(Config.MQTT_BROKER, Config.MQTT_PORT)
#mqttClient.publish(Config.TOPIC_NORMAL + "/" + DEBUG, payload = "logwatch running")

print("tick tock, I am starting up...")
camera = cv2.VideoCapture(0)
cv2.namedWindow('smile')
while(cv2.waitKey(250) != 27):
    result, image = camera.read()
    if result:
        cv2.imshow("smile", image) # This window pops up BEHIND the code window, ha!
smol = cv2.resize(image, (320,240))
result, smol_jpg = cv2.imencode(".jpg", image)
smol_bytes = smol_jpg.tobytes()

print("So be it.")
camera.release()
publish.single(Config.TOPIC_IMAGE, payload=smol_bytes, qos=2,
               hostname=Config.MQTT_BROKER, port=Config.MQTT_PORT)
cv2.destroyAllWindows()

#image = load_image()
#publish.single(Config.TOPIC_IMAGE, payload=image, qos=0,
#               hostname=Config.MQTT_BROKER, port=Config.MQTT_PORT)
msgs = []
with open(logfile, "r") as fp:
    for entry in fp.readlines():
        (level, payload) = parse_log(entry)
        if level:
            qos = 0
            topic = Config.TOPIC_TEXT
            if level == ERROR:
                topic = Config.TOPIC_ALERT # + '/' + level
                qos = 2

                payload = str(datetime.now())
                print(topic, payload)
                sleep(.250)

                msgs.append({
                    'topic': topic,
                    'payload': payload,
                    'qos': qos,
                })
                #client.publish(topic, payload=payload, qos=qos)
publish.multiple(msgs, hostname=Config.MQTT_BROKER, port=Config.MQTT_PORT)
