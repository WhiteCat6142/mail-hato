import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

port = 465
smtp_server = "smtp.gmail.com"
sender_email = "me@gmail.com"
receiver_email = "yours@gmail.com"
password = input("your password: ")



message = MIMEMultipart("alternative")
message["Subject"] = "multipart test"
message["From"] = sender_email
message["To"] = receiver_email

text = "test"
html = """\
<html><body>test</body></html>
"""
message.attach(MIMEText(text, "plain"))
message.attach(MIMEText(html, "html"))
context = ssl.create_default_context()

with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)

#https://realpython.com/python-send-email/
