import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_notification(subject, body):
    smtp_server = 'smtp.qq.com'
    smtp_port = 587
    smtp_username = '1526452932@qq.com'
    smtp_password = 'nnalyjifxrhqfgdi'
    recipient_email = 'ctxx2022@163.com'  # 接收提醒邮件的邮箱地址

    # 创建邮件内容
    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    # 连接 SMTP 服务器并发送邮件
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()  
        server.login(smtp_username, smtp_password)
        server.send_message(msg)


send_notification('汇率提醒', '汇率已经低于 906,请注意。')
