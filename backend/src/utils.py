import base64
import json
import os
from google.cloud import iot_v1
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
from .models import User

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
        attachment.file_content = FileContent(base64.b64encode(image_attachment).decode())
        attachment.file_type = FileType('image/jpeg')
        attachment.file_name = FileName('captured.jpg')
        attachment.disposition = Disposition('attachment')
        attachment.content_id = ContentId('defaultcid')
        message.attachment = attachment
    sg = SendGridAPIClient(config.SENDGRID_API_KEY)
    response = sg.send(message)
    return response.status_code == 202


def get_emails(deviceID):
    return map(lambda x: x.email, db.session.query(User).filter(User.get_alerts == True, User.device_id == deviceID).all())


# The callback for when a PUBLISH message is received from the server.
def broadcast_mail(deviceID, msg):
    for addr in get_emails():
        if send_mail('alarmy@hiding.icu', addr, msg['subject'], msg['content'], msg.get('img_attachment')):
            print('Sent mail')
        else:
            print('Failed to send mail')

def send_hware_config(payload):
    PROJECT_ID = os.getenv("PROJECT_ID")
    REGION = os.getenv("REGION")
    REGISTRY_ID = os.getenv("REGISTRY_ID")
    DEVICE_ID = os.getenv("DEVICE_ID")
    client = iot_v1.DeviceManagerClient()
    device_path = client.device_path(PROJECT_ID, REGION, REGISTRY_ID, DEVICE_ID)

    data = json.dumps(payload).encode('utf-8')
    base64.b64encode(data)
    client.modify_cloud_to_device_config(device_path, data)
    print(f"{payload} successfully sent.")
