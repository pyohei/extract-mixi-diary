"""Parser of mixi diary list"""
import codecs
from html.parser import HTMLParser


class Mixi(HTMLParser):

    values = []
    
    def handle_starttag(self, tag, attrs):
        if tag == 'input':
            a = dict(attrs)
            if 'class' in a and a['class'] == 'JS_checkbox':
                if 'value' in a:
                    self.values.append(a['value'])
                

def parse():
    p = Mixi()
    with codecs.open('test.html', 'r', 'utf-8', 'ignore') as f:
        p.feed(f.read())
    return(p.values)

if __name__ == '__main__':
    main()
