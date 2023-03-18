# https://ideone.com/BLQ2FM
# https://blog.tmtms.net/entry/2015/12/07/mime-header-encoding
# https://docs.python.org/ja/3/library/email.message.html

from email.message import Message
from email.header import Header
msg = Message()
h = Header('MIMEヘッダエンコーディングは複雑すぎてつらい', 'utf-8',77,'Subject')
msg['Subject'] = h.encode()
print(msg.as_string())
print(h.encode())
