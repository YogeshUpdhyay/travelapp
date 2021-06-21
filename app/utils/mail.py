from .. import mail
from flask_mail import Message
from flask import url_for, render_template
import pdfkit

def send_reset_email(user):
    # generates a reset token for the user
    token = user.generate_reset_token()

    # sends the message
    msg = Message('Password Reset Request',
                    sender="noreply@clubmandal.com",
                    recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('user.reset_password', token=token, _external=True)}'''
    mail.send(msg)

def send_membership_mail(user, file_path):
    # defining the message
    msg = Message('Welcome the Club Mandalpatti Family!',
                    sender="noreply@clubmandal.com",
                    recipients=[user.email])
    msg.body = f'''Congratulations on becoming a member of the community
    Please find the attached Id Card. With this id card you can now avail 
    new offers and discounts while joining our events'''

    # attaching the id card
    # renderer = render_template('/utils/idcard.html', image=file_path, user=user)
    # pdf = pdfkit.from_string(renderer, False)
    # msg.attach("idcard.pdf", "pdf", pdf)

    msg.send()

def send_invite_email(user, event):
    pass

def send_event_mail(user, event):
    pass

def send_registration_mail(user):
    # registeration mail
    msg = Message('Welcome the Club Mandalpatti Family!',
                    sender="noreply@clubmandal.com",
                    recipients=[user.email])
    msg.body = f'''Thank you registering with us!
    Here are some coupons to get you started
    COUPON CODE: BIG25 
    Apply this coupon to avial 25% off on memberships'''
    msg.send()