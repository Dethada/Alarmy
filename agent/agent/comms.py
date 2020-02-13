import datetime
import logging
import json
import os
import random
import ssl
import time
import jwt
import paho.mqtt.client as mqtt
from config import config
from events import message_handler
'''
Registry ID: CA2-Registry
Region: asia-east1
'''
# The initial backoff time after a disconnection occurs, in seconds.
minimum_backoff_time = 1

# The maximum backoff time before giving up, in seconds.
MAXIMUM_BACKOFF_TIME = 32

# Whether to wait with exponential backoff before publishing.
should_backoff = False

# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    mqttc.subscribe(config['TMP']['CONFIG_TOPIC'], qos=0)
    mqttc.subscribe(config['TMP']['ALERT_TOPIC'], qos=0)

# The callback for when a PUBLISH message is received from the server.
# def on_message(mqttc, userdata, msg):
#     print(msg.topic+" "+str(msg.payload))

def get_client():
    client = mqtt.Client()
    # client.username_pw_set(
    #         username='unused',
    #         password=create_jwt(
    #                 project_id, private_key_file, 'ES256'))
    
    # # Enable SSL/TLS support.
    # client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # # Connect to the Google MQTT bridge.
    client.connect('127.0.0.1', 1883)

    return client


mqttc = get_client()
mqttc.on_connect = on_connect
mqttc.on_message = message_handler

def publish(topic, data):
    mqttc.publish(f"{config['TMP']['DEVICE_TOPIC']}{topic}", json.dumps(data))

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_start()