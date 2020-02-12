import datetime
import logging
import os
import random
import ssl
import time
import jwt
import paho.mqtt.client as mqtt
from time import sleep

# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # mqttc.subscribe("$SYS/#")

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

    # client.subscribe(mqtt_command_topic, qos=0)

    return client

def on_message(unused_client, unused_userdata, message):
    """Callback when the device receives a message on a subscription."""
    payload = str(message.payload.decode('utf-8'))
    print('Received message \'{}\' on topic \'{}\' with Qos {}'.format(
            payload, message.topic, str(message.qos)))

mqttc = get_client()
mqttc.on_connect = on_connect
mqttc.on_message = on_message

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_start()
sleep(60)
