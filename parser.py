"""Parser of mixi diary list"""
import codecs
from html.parser import HTMLParser

values = []

class Mixi(HTMLParser):

    
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            a = dict(attrs)
            if 'class' in a and a['class'] == 'JS_checkbox':
                if 'value' in a:
                    values.append(a['value'])
                

def parse(file_path):
    p = Mixi()
    with codecs.open(file_path, 'r', 'utf-8', 'ignore') as f:
        p.feed(f.read())
    return(values)

if __name__ == '__main__':
    main()
