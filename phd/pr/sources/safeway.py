import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Safeway(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\d\d)/(\d\d)/12$')

    def get_linkpages(self):
        all_html = []
        url = 'http://phx.corporate-ir.net/phoenix.zhtml?c=64607&p=irol-news&nyo=1'
        html = urlopen(url).read()
        start = html.index('Class="ccbnLnk">2009')
        end = html.index('</html>', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class') and \
                tag.get('class') is not None and tag.get('class')[0] == "ccbnTblLnk" and \
                tag.has_key('onmouseover') and tag.get('onmouseover') is not None

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and \
                tag.get('class') is not None and \
                (tag.get('class')[0] == "ccbnTblOdd" or tag.get('class')[0] == "ccbnTblEven") and \
                tag.string is not None and self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        text = urljoin('http://phx.corporate-ir.net/', link)
        text = text.replace('newsArticle', 'newsArticle_Print')
        return text

    def get_title(self, tag):
        return tag.string

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern')
        year = 2012
        month = int(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<p>')
        end = html.find('<p>SOURCE', start)
        if end == -1:
            end = html.find('<pre>Contact:', start)
        if end == -1:
            end = html.index('<pre>CONTACT:', start)
        html = html[start:end]
        return self._filter_html(html)
