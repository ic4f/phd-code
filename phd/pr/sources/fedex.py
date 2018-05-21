import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Fedex(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d{1,2}) 2012')

    def get_linkpages(self):
        all_html = []
        base = 'http://news.van.fedex.com/archive/2012?page={0}'
        for i in range(0,5):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('view-content')
            end = html.index('class="pager', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'span' and \
            tag.parent.has_key('class') and tag.parent.get('class')[0] == 'field-content'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and tag.parent.name == 'div' and \
                tag.parent.has_key('class') and \
                tag.parent.get('class')[0] == 'views-field-created' and \
                self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        #special handling for fededx:
        if link == '/fedex-ground-names-entrepreneurs-year-1':
                link = '/fedex-ground-names-entrepreneurs-year'
        return urljoin('http://news.van.fedex.com/', link)

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s)
        return ''.join(sb)

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
        start = html.index('<div class="article-body">')
        end = html.index('<div class="terms terms-inline">', start)
        html = html[start:end]
        return self._filter_html(html)
