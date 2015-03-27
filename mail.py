#!usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.MIMEText import MIMEText
from email.Utils import formatdate
from email.Header import Header
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

smtpHost = 'smtp.163.com'
smtpPort = '25'
sslPort  = '465'
fromMail = 'oyjp94@163.com'
toMail   = '527643546@qq.com'
username = 'oyjp94@163.com'
password = 'ca0e04#jk78900'

def send_a_mail(subject, body):
    #初始化邮件
    encoding = 'utf-8'
    mail = MIMEText(body.encode(encoding),'plain',encoding)
    mail['Subject'] = Header(subject,encoding)
    mail['From'] = fromMail
    mail['To'] = toMail
    mail['Date'] = formatdate()

    try:
        #纯粹的ssl加密方式，通信过程加密，邮件数据安全
        smtp = smtplib.SMTP_SSL(smtpHost, sslPort)
        smtp.ehlo()
        smtp.login(username, password)

        #发送邮件
        smtp.sendmail(fromMail, toMail, mail.as_string())
        smtp.close()
        print 'OK'
    except Exception:
        print 'Error: unable to send email'

if __name__ == "__main__":
    send_a_mail(subject = u'Python发送测试', body = u'python测试')