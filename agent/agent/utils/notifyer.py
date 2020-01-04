#!/usr/bin/env python3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail, Attachment, FileContent, FileName,
    FileType, Disposition, ContentId)
import db
from models import User
from config import config

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
    sg = SendGridAPIClient(config.SENDGRID_API_KEY)
    response = sg.send(message)
    return response.status_code == 202


def get_emails():
    return map(lambda x: x.email, db.session.query(User).filter(User.get_alerts == True).all())

# The callback for when a PUBLISH message is received from the server.
def broadcast_mail(msg):
    for addr in get_emails():
        if send_mail(config.FROM_ADDR, addr, msg['subject'], msg['content'], msg.get('img_attachment')):
            print('Sent mail', msg)
        else:
            print('Failed to send mail')
