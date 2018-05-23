"""Extract mixi diary

Created at 2014-07-06.
"""

import urllib2
import urllib
import json
import os


consumer_key = os.environ.get('MIXI_CONSUMER_KEY')
consumer_secret = os.environ.get('MIXI_CONSUMER_SECRET')

print(consumer_key)
print(consumer_secret)
print('OWARI')
quit()

SERVER_STATE_URL = "https://secure.mixi-platform.com/2/token"

s_params = {
        "grant_type": "server_state",
        "client_id": CONSUMER_KEY
        }
s_args = urllib.urlencode(s_params)
s_response = urllib2.urlopen(SERVER_STATE_URL, s_args)
s_content = s_response.read()
print s_content
print type(s_content)
s_result = json.loads(s_content)
server_state = s_result["server_state"]

AUTHORIZE_URL = "https://mixi.jp/connect_authorize.pl"
a_params= {
        "client_id": CONSUMER_KEY,
        "response_type": "code",
        "scope": "r_diary",
        "display": "pc",
        "server_state": server_state,
        "state": ""
        }
a_args = urllib.urlencode(a_params)
a_url = AUTHORIZE_URL + "?" + a_args
print a_url

code = raw_input("input authorize code:")
print code

r_params = {
        "grant_type": "authorization_code",
        "client_id": CONSUMER_KEY,
        "client_secret": CONSUMER_SECRET,
        "code": code,
        "redirect_uri": "http://mixi.jp/connect_authorize_success.html",
        "server_state": server_state
        }
r_args = urllib.urlencode(r_params)
print r_args
r_response = urllib2.urlopen(SERVER_STATE_URL, r_args)
r_content = r_response.read()
print r_content
r_result = json.loads(r_content)
print r_result
ACCESS_TOKEN = r_result["access_token"]

diary_url = "http://api.mixi-platform.com/2/diary/articles/6867209/@self/1695161660"
BODY_FORM ="text/plain"

d_url = diary_url + "?access_token=" + ACCESS_TOKEN
print d_url


d_resp = urllib2.urlopen(d_url)
d_contents = d_resp.read()

print d_contents


