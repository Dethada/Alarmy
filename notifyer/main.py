#!/usr/bin/env python3
import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
import paho.mqtt.client as mqtt
import db
from models import User
from dotenv import load_dotenv
load_dotenv()


FROM_ADDR = 'alarmy@hiding.icu'

def send_mail(sender, recipient, subject, content, image_attachment=None):
    '''
    return true if success, false if failed
    '''
    message = Mail(
        from_email=sender,
        to_emails=recipient,
        subject=subject,
        html_content=content)
    if image_attachment:
        attachment = Attachment()
        attachment.file_content = FileContent(image_attachment)
        attachment.file_type = FileType('image/jpeg')
        attachment.file_name = FileName('captured.jpg')
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('defaultcid')
        message.attachment = attachment
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    return response.status_code == 202


def get_emails():
    return map(lambda x: x.email, db.session.query(User).filter(User.get_alerts == True).all())

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("/alert")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, raw_msg):
    msg = json.loads(raw_msg.payload.decode())
    print(raw_msg.topic, msg['subject'], msg['content'])
    for addr in get_emails():
        if send_mail(FROM_ADDR, addr, msg['subject'], msg['content'], msg.get('img_attachment')):
            print('Sent mail', msg)
        else:
            print('Failed to send mail')

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.17", port=1883, keepalive=60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
