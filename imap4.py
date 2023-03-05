import imaplib
import ssl
import base64
import email.message
import email.parser
import email.policy
import configparser

import auth

# https://stackoverflow.com/questions/25318012/how-to-connect-with-python-imap4-ssl-and-self-signed-server-ssl-cert
# https://docs.python.org/ja/3/library/ssl.html#ssl.PROTOCOL_TLS
# https://learn.microsoft.com/ja-jp/exchange/client-developer/legacy-protocols/how-to-authenticate-an-imap-pop-smtp-application-by-using-oauth
# https://docs.python.org/ja/3/library/email.examples.html
# https://docs.python.org/ja/3/library/email.message.html#email.message.EmailMessage

# https://docs.python.org/ja/3/library/imaplib.html#module-imaplib
# It will be called to process server continuation responses; the response argument it is passed will be bytes. It should return bytes data that will be base64 encoded and sent to the server. It should return None if the client abort response * should be sent instead.

config = configparser.ConfigParser()
config.read('example.ini')
refresh_token=''
if not 'Tokens' in config:
 refresh_token=auth.login()['refresh_token']
else:
 refresh_token=config['Tokens']['refresh_token']
response=auth.RefreshTokens(refresh_token)

ctx = ssl.create_default_context()
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
ctx.maximum_version = ssl.TLSVersion.TLSv1_3
mail =  imaplib.IMAP4_SSL('imap.gmail.com', 993, ssl_context=ctx)

userName=config['User']['name']
accessToken=response['access_token']
mail.authenticate('XOAUTH2',lambda x: ("user=" + userName + "\x01auth=Bearer " + accessToken + "\x01\x01").encode('ascii'))

mail.select('INBOX', 1)
typ, uids = mail.uid("SEARCH", None, "ALL")
uids = uids[0].split()
print(len(uids))
typ, data = mail.fetch(uids[0], '(RFC822)')
msg = email.parser.BytesParser(policy=email.policy.default).parsebytes(data[0][1])
for part in msg.walk():
    print(part.get_content_type())
    print(part.items())
    body=part.get_payload(decode=True)
    if type(body)==bytes:
        charset=part['Content-Type'].params['charset']
        print(charset) 
        print(body.decode(charset or 'UTF-8'))

mail.close()
mail.logout()
