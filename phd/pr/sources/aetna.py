import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Aetna(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\d{1,2})/(\d{1,2})/12 ')

    def get_linkpages(self):
        all_html = []
        base = 'http://newshub.aetna.com/news-releases/all/2012/all?page=0%2C'
        for i in range(0,11):
            url = base + str(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('news/01pridx.htm') + 350
            end = html.index('ul class="pager"', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and not tag.has_key('class') and tag.parent.name == 'span'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and \
            tag.has_key('class') and tag.get('class')[0] == "field-content" and \
            tag.string is not None and self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return urljoin('http://newshub.aetna.com/', link)

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
        start = html.index('<div class="panel-pane pane-node-body" >')
        end = html.find('Contact:          </h2>', start)
        if end == -1:
            end = html.index('<!-- /#bw-content -->', start)

        html = html[start:end]
        return self._filter_html(html)
