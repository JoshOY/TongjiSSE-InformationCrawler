#-*- coding: utf-8 -*-
__author__ = 'JoshOY'

import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

def send_mail(sendinfo, mailobj):
    encoding = 'utf-8'
    try:
        # 初始化邮件，使用SSl
        smtp = smtplib.SMTP_SSL(sendinfo['smtphost'], sendinfo['sslport'])
        smtp.ehlo()
        smtp.login(sendinfo['username'], sendinfo['password'])

        # 发送邮件
        smtp.sendmail(sendinfo['frommail'], sendinfo['tomail'], mailobj.as_string())
        smtp.close()
    except Exception as err:
        print "Exception: Unable to send e-mail."
        print err

def create_sendinfo(smtphost, frommail, tomail, username, password, sslport='465'):
    sendinfo = {}
    sendinfo['smtphost'] = smtphost
    sendinfo['sslport'] = sslport
    sendinfo['frommail'] = frommail
    sendinfo['tomail'] = tomail
    sendinfo['username'] = username
    sendinfo['password'] = password
    return sendinfo

def create_mailobj(subject, body, frommail, tomail, encoding='utf-8'):
    mail = MIMEText(body.encode(encoding), 'plain', encoding)
    mail['Subject'] = Header(subject, encoding)
    mail['From'] =frommail
    mail['To'] = tomail
    mail['Date'] = formatdate()
    return mail