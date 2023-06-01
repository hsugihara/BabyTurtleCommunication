'''ファイルを添付したメールを送信する'''
import sys
import smtplib
from email.mime import multipart
from email.mime import text
from email.mime.application import MIMEApplication

smtp_host = 'smtp.gmail.com'
smtp_port = 587

from_email = 'bt@edgematrix.com'
# to_email = 'hsugihara@edgematrix.com'
username = 'bt@edgematrix.com'
app_password = 'yqkbbajkftaeurxf'

msg = multipart.MIMEMultipart()
msg['Subject'] = 'log files from bt-01'
msg['From'] = from_email
# msg['To'] = to_email
msg.attach(text.MIMEText('Test email', 'plain'))        # 本文

# TODO: 送出する　ファイル名はシェルスクリプトからもらう引数にする
# 送出先も引数でもらう（一つだけ）

# check argument number
args = sys.argv
if 3 != len(args):
    print('Require two arguments, file name and to_email address')
    exit(1)

# set file name and to_email
attachedfilename = args[1]
to_email = args[2]
msg['To'] = to_email

try:
    with open(attachedfilename, 'rb') as f:
        attachment = MIMEApplication(f.read())
        attachment.add_header(
            'Content-Disposition', 'attachment',
            filename=attachedfilename
        )
        msg.attach(attachment)
except Exception as e:
    print(f'[ERROR] {type(e)}:{str(e)}')
    exit(1)


# attach bt id file (bt_id.txt)
try:
    with open('bt_id.txt', 'r') as f:
        attachment = text.MIMEText(f.read())
        attachment.add_header(
            'Content-Disposition', 'attachment',
            filename='bt_id.txt'
        )
        msg.attach(attachment)
except Exception as e:
    print(f'[ERROR] {type(e)}:{str(e)}')
    exit(1)


server = smtplib.SMTP(smtp_host, smtp_port)
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, app_password)
server.send_message(msg)
server.quit()