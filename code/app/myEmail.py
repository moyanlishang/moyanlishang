# -*- coding:utf8 -*-
from email.MIMEText import MIMEText
import smtplib
from threading import Thread
from flask import current_app, render_template


class SendEmail:
    # 构造函数：初始化基本信息
    def __init__(self, host, user, passwd):
        lInfo = user.split("@")
        self._user = user
        self._account = lInfo[0]
        self._me = self._account + "<" + self._user + ">"

        server = smtplib.SMTP()
        server.connect(host, 25)
        server.login(self._account, passwd)
        self._server = server

    # 发送文件或html邮件
    def sendTxtMail(self, to_list, sub, content, subtype='html'):
        # 如果发送的是文本邮件，则_subtype设置为plain
        # 如果发送的是html邮件，则_subtype设置为html
        msg = MIMEText(content, _subtype=subtype, _charset='utf-8')
        msg['Subject'] = sub
        msg['From'] = self._me
        msg['To'] = ";".join(to_list)
        self._server.sendmail(self._me, to_list, msg.as_string())
        return True

    # 析构函数：释放资源
    def __del__(self):
        self._server.quit()
        self._server.close()

class Async_email_Thread(Thread):
    def __init__(self, app, to, subject, template, **kwargs):
        self.mailto_list = [to]
        self.mail = SendEmail(app.config['MAIL_SERVER'], app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        self.html = render_template(template + '.html', **kwargs)
        self.subject = subject
        Thread.__init__(self)

    def run(self):
        if self.mail.sendTxtMail(self.mailto_list, self.subject, self.html):
            print "发送成功"
        else:
            print "发送失败"

def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    thr = Async_email_Thread(app, to, subject, template, **kwargs)
    thr.start()
    return thr


