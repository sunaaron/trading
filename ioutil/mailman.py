'''
Created on Nov 10, 2017

@author: Aaron
'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tools import dateutil, misc

conf = misc.get_conf()

def send_email(subject, html_message):
    gmail_user = conf["from_user"]
    gmail_pwd = conf["gmail_pwd"]
    FROM = gmail_user
    TO = conf["to_users"] 
    
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

def gen_daily_screen_subject(symbol_lst):
    subject = "Daily Finviz Summary- %s" % dateutil.get_today_date()
    return "%s - with total selections %d" % (
            subject, len(symbol_lst))

def gen_daily_watch_subject(watch_type):
    return "Daily %s Watch List - %s" % (
            watch_type, dateutil.get_today_date())

def gen_correlation_subject():
    return "Side-to-side correlation inspection"

