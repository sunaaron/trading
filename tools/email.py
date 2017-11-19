'''
Created on Nov 10, 2017

@author: Aaron
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, html_message):
    gmail_user = "aaron.sun82@gmail.com"
    gmail_pwd = "2wsx#EDC"
    FROM = gmail_user
    TO = [gmail_user] 
    
    # Create message container - the correct MIME type is multipart/alternative.
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(MIMEText(html_message, 'html'))

    try:
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_pwd)
        smtpserver.sendmail(FROM, TO, msg.as_string())
        smtpserver.close()
        print 'Successfully sent the mail'
    except Exception, e:
        print e
        raise
