"""Parser of mixi diary list

This script enable to parse mixi diary id from diary list pages.
To use this, you execute parse function with file path which having mixi diary id.
After executing, you can access the list of mixi diary id as `values` variables.

*Attention*
  This script save mixi diary id as module variables.
  And `values` variable don't reset in same instance.
"""
import codecs
from html.parser import HTMLParser

values = []

class Mixi(HTMLParser):
    
    def handle_starttag(self, tag, attrs):
        """Parse mixi diary id."""
        if tag == 'input':
            a = dict(attrs)
            if 'class' in a and a['class'] == 'JS_checkbox':
                if 'value' in a and a['value'] not in values:
                    values.append(a['value'])
                

def parse(file_path):
    """Parse file."""
    p = Mixi()
    with codecs.open(file_path, 'r', 'utf-8', 'ignore') as f:
        p.feed(f.read())
