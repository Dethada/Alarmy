from time import sleep
import paho.mqtt.client as mqtt

device_topic = 'devices/device1/'

# The callback for when the client receives a CONNACK response from the server.
def on_connect(mqttc, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    print(f'{device_topic}config')
    mqttc.subscribe('config', qos=0)

def get_client():
    client = mqtt.Client()

    # Connect to the Google MQTT bridge.
    client.connect('127.0.0.1', 1883)

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
mqttc.loop_forever()
# sleep(60)