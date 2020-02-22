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

def create_jwt(project_id, private_key_file, algorithm):
    """Creates a JWT (https://jwt.io) to establish an MQTT connection.
        Args:
         project_id: The cloud project ID this device belongs to
         private_key_file: A path to a file containing either an RSA256 or
                 ES256 private key.
         algorithm: The encryption algorithm to use. Either 'RS256' or 'ES256'
        Returns:
            A JWT generated from the given project_id and private key, which
            expires in 20 minutes. After 20 minutes, your client will be
            disconnected, and a new JWT will have to be generated.
        Raises:
            ValueError: If the private_key_file does not contain a known key.
        """
    token = {
            # The time that the token was issued at
            'iat': datetime.datetime.utcnow(),
            # The time the token expires.
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            # The audience field should always be set to the GCP project id.
            'aud': project_id
    }

    # Read the private key file.
    with open(private_key_file, 'r') as f:
        private_key = f.read()

    print('Creating JWT using {} from private key file {}'.format(
            algorithm, private_key_file))

    return jwt.encode(token, private_key, algorithm=algorithm)

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
    project_id, cloud_region, registry_id, gateway_id = config['PROJECT_ID'], config['REGION'], config['REGISTRY_ID'], config['GATEWAY_ID']
    client_id = 'projects/{}/locations/{}/registries/{}/devices/{}'.format(
            project_id, cloud_region, registry_id, gateway_id)
    print('Device client_id is \'{}\''.format(client_id))
    priv_key_path = config['PRIVATE_KEY_PATH']
    client = mqtt.Client(client_id=client_id)
    client.username_pw_set(
        username='unused',
        password=create_jwt(
        project_id, priv_key_path, 'RS256'))
    
    # # Enable SSL/TLS support.
    ca_certs = config['CA_PATH']
    client.tls_set(ca_certs=ca_certs, tls_version=ssl.PROTOCOL_TLSv1_2)

    # # Connect to the Google MQTT bridge.
    client.connect('mqtt.googleapis.com', 8883)

    return client

def attach_device(client, device_id, auth):
    """Attach the device to the gateway."""
    attach_topic = '/devices/{}/attach'.format(device_id)
    attach_payload = '{{"authorization" : "{}"}}'.format(auth)
    client.publish(attach_topic, attach_payload, qos=1)

mqttc = get_client()
mqttc.on_connect = on_connect
mqttc.on_message = message_handler
attach_device(mqttc,config['DEVICE_ID'],'')

def publish(topic, data):
    print(f"/{config['TMP']['DEVICE_TOPIC']}{topic}")
    mqttc.publish(f"/{config['TMP']['DEVICE_TOPIC']}{topic}", json.dumps(data),qos=1)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqttc.loop_start()
