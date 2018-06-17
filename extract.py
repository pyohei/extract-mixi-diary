# FLOW
#  Get access token from localhost
#  request 
#  save
#  loop

import requests

ACCESS_KEY = '0ad4afda3cdf98e50b6357e0adcc35427735c83f'

def get_diary(diary_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'access_token': ACCESS_KEY}
    url = 'http://api.mixi-platform.com/2/diary/articles/@me/@self/{}/'
    r = requests.get(url.format(str(diary_id)), params=params, headers=headers)
    print(r)
    print(r.json())
    c = r.json()['created']
    with open(c, 'w') as f:
        f.write(r.text)
    print('finish')

    
    

get_diary(1721036643)
