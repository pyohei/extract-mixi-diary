"""Get and save mixi diary."""
import os
import requests


class Extractction(object):

    def __init__(self, port, save_dir):
        self.port = port
        self.save_dir = save_dir

    def _get_access_token(self):
        """Get access token from localhost.

        This script load access token from server.py result.
        Therefore, you must run server.py to obtain access token.
        See README.md.
        """
        try:
            r = requests.get('http://localhost:{}'.format(self.port))
            return r.text
        except Exception as e:
            print('You have trouble to fetch access token(localhost)')
            print('If you do not run server, please execute `server.py`.')
            print('<-------PythonError------>')
            print(e)
            raise

    def save_diary(self, diary_id):
        """Get and save mixi diary."""
        access_token = self._get_access_token()
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'access_token': access_token}
        url = 'http://api.mixi-platform.com/2/diary/articles/@me/@self/{}/'
        r = requests.get(url.format(str(diary_id)), params=params, headers=headers)
        # Debug
        print(r)
        print(r.json())
        c = r.json()['created']
        n = self._create_file_name(c)
        print(n) # Debug

        with open(n, 'w') as f:
            f.write(r.text)

    def _create_file_name(self, created):
        """Create file neme as YYYYmmddHHMMDD.json'"""
        f = '{}.json'.format(
                created.replace('-', '').replace(':', '').replace('T', '')[0:14])
        p = os.path.join(self.save_dir, f)
        return p
    
if __name__ == '__main__':
    # This is test for myself.
    e = Extractction(9999, '/tmp')
    e.save_diary(1721036643)
