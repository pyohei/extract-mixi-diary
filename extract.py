"""Get and save mixi diary."""
import requests

ACCESS_KEY = 'fd44abc91c7356584a5c6116de2060401766c17f'

def get_diary(diary_id):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    params = {'access_token': ACCESS_KEY}
    url = 'http://api.mixi-platform.com/2/diary/articles/@me/@self/{}/'
    r = requests.get(url.format(str(diary_id)), params=params, headers=headers)
    print(r)
    print(r.json())
    c = r.json()['created']
    n = _create_file_name(c)
    print(n)

    with open(n, 'w') as f:
        f.write(r.text)
    print('finish')

def _create_file_name(created):
    """Create file neme as YYYYmmddHHMMDD.json'"""
    return '{}.json'.format(
            created.replace('-', '').replace(':', '').replace('T', '')[0:14])
    
if __name__ == '__main__':
    get_diary(1721036643)
