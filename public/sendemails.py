# -*- coding: UTF-8 -*-
import os
import time
import smtplib
from email.utils import parseaddr, formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from public.PublicMethod import PublicMethod


class SendEmails:

    # 将邮件的name转换成utf-8格式
    def _format_addr(s):
        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))

    def sendemails(self, attachment):
        apk_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        data = PublicMethod().operateYaml(apk_path + "/data/Login.yaml")  # 读取yaml数据表的值
        username = data['Setting']['sendemail']['username']  # 邮件服务器登录名
        password = data['Setting']['sendemail']['password']  # 邮件服务器密码
        sender = data['Setting']['sendemail']['sender']  # 邮件的发送者
        receivers = data['Setting']['sendemail']['receivers']  # 邮件的接收者
        to_addr = data['Setting']['sendemail']['receivers']  # 邮件的接收者

        msg = MIMEMultipart()
        error = PublicMethod().analysis_log()[0]
        error_tip = "本次测试log文件中存在error，请检查\n"
        warning = PublicMethod().analysis_log()[1]
        warning_tip = "本次测试log文件中存在warning，请检查\n"
        died = PublicMethod().analysis_log()[2]
        died_tip = "本次测试log文件中存在闪退或程序卡死，请检查"
        body = 'APK大厅自动化测试已完成，请查看附件\n'
        if error == 1:
            body = body + error_tip
        if warning == 1:
            body = body + warning_tip
        if died == 1:
            body = body + died_tip
        if error == 1 or warning == 1 or died == 1:
            pass
        else:
            day = time.strftime('%m%d', time.localtime(time.time()))
            os.remove("jjlog_lua_" + day + ".log")
        msg.attach(MIMEText(body, 'plain', 'utf-8'))  # 定制邮件的正文内容
        msg['From'] = SendEmails._format_addr(u'自动化服务小组<%s>'%username)  # 格式化发送者名称
        msg['To'] = ','.join(to_addr)  # 格式化接收者名称

        subject = 'APK大厅自动化测试报告'
        msg['Subject'] = Header(subject, 'utf-8')  # 定制邮件的主题及格式
        contype = 'application/octet-stream'
        maintype, subtype = contype.split('/', 1)
        (filepath, tempfilename) = os.path.split(attachment)  # 拆分传入的文件路径，获得文件名
        with open(attachment, 'rb') as f:
            # MIMEBase表示附件的对象
            mime = MIMEBase(maintype, subtype, filename=attachment)
            # filename是显示附件名字
            mime.add_header('Content-Disposition', 'attachment', filename=tempfilename)
            # 获取附件内容
            mime.set_payload(f.read())
            encoders.encode_base64(mime)
            # 作为附件添加到邮件
            msg.attach(mime)

        try:
            smtpObj = smtplib.SMTP('smtp.mail.jj.cn', 25)  # 指定邮件服务器及端口
            smtpObj.login(username, password)  # 使用用户名和密码登录服务器
            smtpObj.sendmail(sender, receivers,  msg.as_string())  # 传入发送者，接受者及内容发送邮件
            print("邮件发送成功")
            smtpObj.quit()
        except smtplib.SMTPException:
            print("Error: 无法发送邮件")