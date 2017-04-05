#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import traceback
import handler

'''
  邮件发送
'''

class Send_Email(object):
    def __init__(self, accounts, current_users):
        self.mail_host = 'smtp.exmail.qq.com'
        self.mail_user = 'ads_reporting@newborntown.com'
        self.mail_pass = '5igmKD3F0cLScrS5'
        self.mailto_list = accounts
        # self.sub = "Offer 创建任务" % current_users
        self.sub = "Offer 创建任务 by %s" % current_users

    def send_mail(self,contents):
        me = self.mail_user
        msg = MIMEMultipart()
        msg['Subject'] = self.sub
        msg['From'] = me
        msg['To'] = ",".join(self.mailto_list)

        context = MIMEText(handler.entry(contents), _charset='utf-8')  # 解决乱码
        msg.attach(context)

        try:
            send_smtp = smtplib.SMTP()
            send_smtp.connect(self.mail_host)
            send_smtp.login(self.mail_user, self.mail_pass)
            send_smtp.sendmail(me, self.mailto_list, msg.as_string())
            send_smtp.close()
            return True
        except Exception as e:
            print (traceback.format_exc())
            return False

if __name__ == '__main__':
    obj = Send_Email()
    if obj.send_mail():
        print ("Send mail succed!")
    else:
        print ("Send mail failed!")

