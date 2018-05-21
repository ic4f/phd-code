import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common
from bs4 import BeautifulSoup
from base_source import BaseSource


class Exxon(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\d{1,2})/(\d{1,2})/(1\d)')

    def get_linkpages(self):
        all_html = []
        base = 'http://news.exxonmobil.com/newsroom_homepage?page=0%2C{0}'
        for i in range(0, 8):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('<li class="views-row views-row-1 ')
            end = html.index('<div class="item-list"><ul class="pager">', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    #<div class="views-field-item views-field-title"><span class="field-content">
    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.has_key('class') and \
                tag.parent.get('class')[0] == 'field-content' and \
                tag.parent.parent.name == 'div' and tag.parent.parent.has_key('class') and \
                tag.parent.parent.get('class')[0] == 'views-field-item' and \
                tag.parent.parent.get('class')[1] == 'views-field-title'
    

    def is_title(self, tag):
        return self.is_link(tag)

    #<div class="views-field-item views-field-created"><span class="field-content">
    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and \
                tag.get('class')[0] == 'field-content' and \
                tag.parent.name == 'div' and tag.parent.has_key('class') and \
                tag.parent.get('class')[0] == 'views-field-item' and \
                tag.parent.get('class')[1] == 'views-field-created' and \
                self._ptn_date.match(tag.string.strip())


    def get_link(self, link):
        return urljoin('http://news.exxonmobil.com/', link)

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
        year = 2000 + int(match.group(3))
        month = int(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.find('XOM</div>') + 9
        if start == 8:
            start = html.index('<div class="bw-toolbar">')
        end = html.find('Contact:          </h2>', start)
        if end == -1:
            end = html.index('<div class="bw-sidebar">', start)
        html = html[start:end]

        return self._filter_html(html)
