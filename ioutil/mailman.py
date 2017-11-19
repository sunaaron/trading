'''
Created on Nov 10, 2017

@author: Aaron
'''
import smtplib
from context import constants
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

def gen_daily_subject(symbol_lst):
    subject = "Daily Finviz Summary- %s" % dateutil.get_today_date()
    return "%s - with total selections %d" % (
            subject, len(symbol_lst))

def gen_daily_summary_html(symbol_lst):
    html_str = '<html><head>'
    html_str += '<body><table>'
    
    for symbol_obj in symbol_lst:
        html_str += '<tr>'
        html_str += '<td>%s' % symbol_obj.screen_html_str()
        html_str += '</td></tr>'
        img_src = constants.finviz_img_url % symbol_obj.symbol
        html_str += '<tr><td><img src=' + img_src
        html_str += ' width="67%" height="67%"/></td></tr>'
        
    html_str += '</table></body></head></html>'
    return html_str