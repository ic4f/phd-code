import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Wellpoint(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d\d), 2012')

    def get_linkpages(self):
        all_html = []
        url = 'http://ir.wellpoint.com/phoenix.zhtml?c=130104&p=irol-news&nyo=1'
        print 'collecting links from {0}'.format(url)
        html = urlopen(url).read()
        start = html.index('ccbnLnk">2003')
        end = html.index('ccbnIRQuoteSymbol', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class') and \
                tag.get('class') is not None and tag.get('class')[0] == "ccbnTblLnk"
                
    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and \
                tag.get('class') is not None and \
                (tag.get('class')[0] == "ccbnTblOdd" or tag.get('class')[0] == "ccbnTblEven") and \
                tag.string is not None and self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return urljoin('http://ir.wellpoint.com/',  link)

    def get_title(self, tag):
        return tag.string

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern')
        year = 2012
        month = common.get_month_by_name(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<span class="ccbnNewsTtl">')
        end = html.find('<p>Source: ', start)
        if end == -1:
            end = html.index('<div class="content_Footer">', start)
        html = html[start:end]
        return self._filter_html(html)
