#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os
from .china_time import ChinaTime
import markdown

def send_email(title="fast-retreat-53401.herokuapp", \
               content="msg", content_type = "plain"):
    # 第三方 SMTP 服务
    mail_host = "smtp.qq.com"  # 设置服务器
    mail_user = os.environ.get('MAIL_USER') # 用户名
    mail_pass = os.environ.get('MAIL_PASS')

    sender = mail_user
    receivers = [mail_user]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    now = ChinaTime().getChinaTime()
    text = content+'\n Heroku Python 邮件发送测试...\n'+now
    if type == 'html':
        text = markdown.markdown(text)
    message = MIMEText( text,content_type, 'utf-8' )
    message['From'] = Header( title, 'utf-8' )
    message['To'] = Header( "测试", 'utf-8' )

    subject = 'Heroku Python SMTP 邮件测试'
    message['Subject'] = Header( subject, 'utf-8' )

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect( mail_host, 25 )  # 25 为 SMTP 端口号
        smtpObj.login( mail_user, mail_pass )
        smtpObj.sendmail( sender, receivers, message.as_string() )
        print(now+' 邮件发送成功')

    except smtplib.SMTPException:
        print(now+" Error: 无法发送邮件")

if __name__ == '__main__':
    send_email(title='测试邮件标题',content='测试邮件内容')