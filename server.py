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
import logging
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

# Logging settings
logging.basicConfig(format='%(asctime)s,%(levelname)s,%(message)s',
                    level=logging.INFO)

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """Action of GET protocol.

        Any GET access thorough this process.
        """
        global ACCESS_TOKEN
        u = urlparse(self.path)

        # Redirect process
        if not ACCESS_TOKEN and 'redirect' in u.path:
            code = parse_qs(u.query)['code']
            ACCESS_TOKEN = _get_access_token(code[0])
            logging.info('NewAccessToken:{}'.format(ACCESS_TOKEN))

        # Request new access token
        if not ACCESS_TOKEN:
            r_url = _get_redirect_url()
            self.send_response(301)
            self.send_header('Location', r_url)
            self.end_headers()
            logging.info('RedirectUrl:{}'.format(r_url))
            return

        # Refresh access token
        if TOKEN_EXPIRED:
            rest_time = TOKEN_EXPIRED - time.time()
            if rest_time <= 0:
                ACCESS_TOKEN = _republish_access_token()
            logging.info('RefreshAccessToken:{}({}s)'.format(ACCESS_TOKEN, str(rest_time)))

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('{}'.format(ACCESS_TOKEN).encode('utf-8'))


def _get_server_state():
    """Get server state from mixi API."""
    global SERVER_STATE
    if SERVER_STATE:
        return SERVER_STATE

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'server_state',
              'client_id': CONSUMER_KEY}
    # Do not delete sleep statement!
    time.sleep(2)
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    logging.info('ServerStateResponse:{}'.format(r.text))
    SERVER_STATE = r.json()['server_state']
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
    # Do not delete sleep statement!
    time.sleep(2)
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    response = r.json()
    logging.info('TokenApiResponse:{}'.format(response))

    TOKEN_EXPIRED = int(time.time()) + int(response['expires_in'])
    REFRESH_TOKEN = response['refresh_token']

    return response['access_token']


def _republish_access_token():
    """Get access token from refresh token.
    
    This script is basically same with `_get_access_token()`
    """
    global REFRESH_TOKEN 
    global TOKEN_EXPIRED
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'grant_type': 'refresh_token',
              'client_id': CONSUMER_KEY,
              'client_secret': CONSUMER_SECRET,
              'refresh_token': REFRESH_TOKEN}
    # Do not delete sleep statement!
    time.sleep(2)
    r = requests.post(
            MIXI_TOKEN_URL,
            headers=headers,
            data=params)
    response = r.json()
    logging.info('ReTokenApiResponse:{}'.format(response))

    TOKEN_EXPIRED = int(time.time()) + int(response['expires_in'])
    REFRESH_TOKEN = response['refresh_token']

    return response['access_token']

def _get_redirect_url():
    """Get redirect url.
    
    In this code, I give authorization of reading diary.
    """
    ss = _get_server_state()
    # TODO: want to fix smart code...
    url = '{url}?'\
          'client_id={cid}&'\
          'response_type=code'\
          '&scope=r_diary%20w_diary&'\
          'state=mixiapi&'\
          'server_state={ss}'
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
    args = p.parse_args()
    global CONSUMER_KEY
    global CONSUMER_SECRET
    CONSUMER_KEY = args.consumer
    CONSUMER_SECRET = args.secret

    handler = MyHandler
    httpd = socketserver.TCPServer(("", 9999), handler)
    
    logging.info('http://localhost:{}'.format(9999))
    httpd.serve_forever()

run()
