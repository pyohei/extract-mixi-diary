"""Mixi access token hold server

Only you do is to set your consumer key and secret key in environment.
I confirm this script with Python3.6 only.
"""

# TODO: 
# Republish access token
# timer function
# error handling?(minimum)
import argparse
from http.server import SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler
import socketserver
import io
from urllib.parse import urlparse, parse_qs
import requests
import time

CONSUMER_KEY = None
CONSUMER_SECRET = None
MIXI_TOKEN_URL = 'https://secure.mixi-platform.com/2/token'
MIXI_AUTHORIZATION_URL = 'https://mixi.jp/connect_authorize.pl'
ACCESS_TOKEN = None
SLEEPING_TIME = 1

TOKEN_EXPIRED = None
REFRESH_TOKEN = None


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        global ACCESS_TOKEN
        # TODO: check redirect path.
        # 
        # first
        # create server status
        # redirect autherize path
        # having specific path
        # get code
        # access to access token
        # get access token
        u = urlparse(self.path)
        if not ACCESS_TOKEN and 'redirect' in u.path:
            print(u)
            code = parse_qs(u.query)['code']
            print(code)
            # get access token
            time.sleep(5)
            ACCESS_TOKEN = _get_access_token(code[0])

        print(urlparse(self.path))
        print(self.path)
        #if self.trim_path() = 'redirect':
        if not ACCESS_TOKEN:
            print('GET NEW ACCESS TOKEN!')
            # get server_state
            print(_get_redirect_url())
            self.send_response(301)
            self.send_header('Location', _get_redirect_url())
            self.end_headers()
            return

        global TOKEN_EXPIRED
        if TOKEN_EXPIRED:
            rest_time = TOKEN_EXPIRED - time.time()
            print(rest_time)
            if rest_time <= 0:
                ACCESS_TOKEN = _republish_access_token()

        # response
        #self.send_response(301)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        #self.send_header('Location', 'https://google.com')
        self.end_headers()
        self.wfile.write('{}'.format(ACCESS_TOKEN).encode('utf-8'))

SERVER_STATE = None
def _get_server_state():
    global SERVER_STATE
    if SERVER_STATE:
        print('exits')
        return SERVER_STATE
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'server_state',
              'client_id': CONSUMER_KEY}
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    print(r.text)
    SERVER_STATE = r.json()['server_state']
    print(SERVER_STATE)
    time.sleep(5)
    return SERVER_STATE
# save server state

def _get_access_token(code):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'authorization_code',
              'client_id': CONSUMER_KEY,
              'client_secret': CONSUMER_SECRET,
              'code': code,
              'server_state': SERVER_STATE}
    print(params)
    time.sleep(5)
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    response = r.json()
    print(response)

    global TOKEN_EXPIRED
    TOKEN_EXPIRED = int(time.time()) + int(response['expires_in'])
    global REFRESH_TOKEN 
    REFRESH_TOKEN = response['refresh_token']

    return response['access_token']


def _republish_access_token():
    global REFRESH_TOKEN 
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'refresh_token',
              'client_id': CONSUMER_KEY,
              'client_secret': CONSUMER_SECRET,
              'refresh_token': REFRESH_TOKEN}
    print('Refresh!!!!!!!!!!!!!')
    print(params)
    

    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    response = r.json()
    print(response)

    global TOKEN_EXPIRED
    TOKEN_EXPIRED = int(time.time()) + int(response['expires_in'])
    REFRESH_TOKEN = response['refresh_token']

    return response['access_token']

def _get_redirect_url():
    ss = _get_server_state()
    # I hope to clean this code...
    url = '{url}?client_id={cid}&response_type=code&scope=r_diary%20w_diary&state=mixiapi&server_state={ss}'
    return url.format(
            url=MIXI_AUTHORIZATION_URL,
            cid=CONSUMER_KEY,
            ss=ss)

def run():
    """Run server"""
    p = argparse.ArgumentParser(description='Mixi diary save script.')
    p.add_argument('--consumer', '-c', help='consumer key', required=True)
    p.add_argument('--secret', '-s', help='secret key', required=True)
    p.add_argument('--port', '-p', help='port number of access key', required=True, type=int)
    args = p.parse_args()
    global CONSUMER_KEY
    global CONSUMER_SECRET
    CONSUMER_KEY = args.consumer
    CONSUMER_SECRET = args.secret

    handler = MyHandler
    httpd = socketserver.TCPServer(("", args.port), handler)
    
    print('http://localhost:{}'.format(args.port))
    httpd.serve_forever()

run()
