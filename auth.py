import urllib.request
import urllib.parse
import json
import base64
import hashlib
import ssl
import configparser
import http.server

# https://developers.google.com/identity/protocols/oauth2/web-server?hl=ja#python
# https://github.com/googleapis/google-api-nodejs-client
# https://github.com/google/gmail-oauth2-tools/blob/master/python/oauth2.py
# https://stackoverflow.com/questions/18444395/basehttprequesthandler-with-custom-instance

# https://github.com/WhiteCat6142/gmail-oauth2

config = configparser.ConfigParser()
config.read('example.ini')

client_id=config['Client']['client_id']
client_secret=config['Client']['client_secret']

def AccessTokens(code,code_verifier):
  params = {'code':code,
    'client_id':client_id,
    'client_secret':client_secret,
    'redirect_uri':'http://localhost:9004/oauth2',
    'code_verifier':code_verifier,
    'grant_type':'authorization_code'}
  request_url = 'https://oauth2.googleapis.com/token'

  response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('ascii')).read().decode('utf-8')
  return json.loads(response)

def RefreshTokens(refresh_token):
  params = {'client_id':client_id,
    'client_secret':client_secret,
    'refresh_token':refresh_token,
    'grant_type':'refresh_token'}
  request_url = 'https://oauth2.googleapis.com/token'

  response = urllib.request.urlopen(request_url, urllib.parse.urlencode(params).encode('ascii')).read().decode('utf-8')
  return json.loads(response)

def login():
  code_verifier=ssl.RAND_bytes(16).hex()
  m=hashlib.sha256()
  m.update(code_verifier.encode('ascii'))
  #omit padding
  code_challenge=base64.urlsafe_b64encode(m.digest()).decode('ascii')[0:-1]

  print('Open https://accounts.google.com/o/oauth2/v2/auth?scope=https%3A//mail.google.com/&response_type=code&redirect_uri=http%3A//localhost%3A9004/oauth2&client_id='+client_id+'&code_challenge='+code_challenge+'&code_challenge_method=S256')

  server = http.server.HTTPServer(('', 9004), myHandler)
  server.t1 = {'code_verifier':code_verifier}
  while not 'response' in server.t1:
    server.handle_request()
  refresh_token=server.t1['response']['refresh_token']
  config['Tokens']={'refresh_token':refresh_token}
  with open('example.ini', 'w') as f:
    config.write(f)
  return server.t1['response']
  
class myHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    if not self.path.startswith('/oauth2'):
      self.send_response(404)
      self.end_headers()
      return
    query=urllib.parse.parse_qs(self.path[8:])
    self.send_response(200)
    self.send_header('Content-type','text/html')
    self.end_headers()

    code=query['code'][0]
    code_verifier=self.server.t1['code_verifier']
    response=AccessTokens(code,code_verifier)
    self.server.t1['response'] = response
    self.wfile.write('ok'.encode('utf-8'))
    return

if __name__ == '__main__':
    print(login())


