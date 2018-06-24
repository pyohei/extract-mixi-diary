"""Mixi access token holding server

Only you do is to set your consumer key and secret key in environment.
I confirm this script with Python3.6 only.

This script specialize in reading mixi diary.
You must change scope if you want to have another authorization.
If you want to know more, please read README.md.
"""
import argparse
from http.server import SimpleHTTPRequestHandler
from http.server import BaseHTTPRequestHandler
import socketserver
import io
from urllib.parse import urlparse, parse_qs
import requests
import time

# Settings
CONSUMER_KEY = None
CONSUMER_SECRET = None
MIXI_TOKEN_URL = 'https://secure.mixi-platform.com/2/token'
MIXI_AUTHORIZATION_URL = 'https://mixi.jp/connect_authorize.pl'
ACCESS_TOKEN = None
SLEEPING_TIME = 1
TOKEN_EXPIRED = None
REFRESH_TOKEN = None
SERVER_STATE = None


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Action of GET protocol.

        Any GET access thorough this process.
        """
        global ACCESS_TOKEN

        u = urlparse(self.path)
        # TODO: logging
        print(self.path)
        print(urlparse(self.path))
        if not ACCESS_TOKEN and 'redirect' in u.path:
            # TODO: logging
            print(u)
            print(code)
            code = parse_qs(u.query)['code']
            time.sleep(2)
            ACCESS_TOKEN = _get_access_token(code[0])

        if not ACCESS_TOKEN:
            # TODO: logging
            print('GET NEW ACCESS TOKEN!')
            # get server_state
            print(_get_redirect_url())
            self.send_response(301)
            self.send_header('Location', _get_redirect_url())
            self.end_headers()
            return

        if TOKEN_EXPIRED:
            # TODO: logging
            print(rest_time)
            rest_time = TOKEN_EXPIRED - time.time()
            if rest_time <= 0:
                ACCESS_TOKEN = _republish_access_token()

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('{}'.format(ACCESS_TOKEN).encode('utf-8'))

# NOTE: I think the below scripts should include in class??
def _get_server_state():
    """Get server state from mixi API."""
    global SERVER_STATE
    if SERVER_STATE:
        # TODO: logging
        print('exits')
        return SERVER_STATE
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'server_state',
              'client_id': CONSUMER_KEY}
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    # TODO: logging
    print(r.text)
    SERVER_STATE = r.json()['server_state']
    time.sleep(2)
    return SERVER_STATE

def _get_access_token(code):
    """Get access token from mixi API"""
    global TOKEN_EXPIRED
    global REFRESH_TOKEN 
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'authorization_code',
              'client_id': CONSUMER_KEY,
              'client_secret': CONSUMER_SECRET,
              'code': code,
              'server_state': SERVER_STATE}
    time.sleep(5)
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    response = r.json()
    # TODO: logging
    print(response)

    TOKEN_EXPIRED = int(time.time()) + int(response['expires_in'])
    REFRESH_TOKEN = response['refresh_token']

    return response['access_token']


def _republish_access_token():
    """Get access token from refresh token."""
    global REFRESH_TOKEN 
    global TOKEN_EXPIRED
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'refresh_token',
              'client_id': CONSUMER_KEY,
              'client_secret': CONSUMER_SECRET,
              'refresh_token': REFRESH_TOKEN}
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    response = r.json()
    # TODO: logging
    print(params)
    print(response)

    TOKEN_EXPIRED = int(time.time()) + int(response['expires_in'])
    REFRESH_TOKEN = response['refresh_token']

    return response['access_token']

def _get_redirect_url():
    """Get redirect url.
    
    In this code, I give authorization of reading diary.
    """
    ss = _get_server_state()
    url = '{url}?client_id={cid}&response_type=code&scope=r_diary%20w_diary&state=mixiapi&server_state={ss}'
    return url.format(
            url=MIXI_AUTHORIZATION_URL,
            cid=CONSUMER_KEY,
            ss=ss)

def run():
    """Run server
    
    The main script this module.
    You have to give mixi consumer key and cosumer secret when running this script.
    """
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
