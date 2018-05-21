import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Boa(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('[\w\s]+ - (\w+) (\d{1,2}), 2012')

    def get_linkpages(self):
        all_html = []
        base = 'http://newsroom.bankofamerica.com/advsearch?page={0}&date_from=2012-01-01T00%3A00%3A00Z&date_to=2013-01-01T00%3A00%3A00Z&year=2012'
        for i in range(0,30):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('<h2>Search results</h2>')
            end = html.index('<ul class="pager">', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'dt' and \
            tag.parent.has_key('class') and tag.parent.get('class')[0] == 'title'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'p' and tag.has_key('class') and \
                tag.get('class')[0] == 'search-info' and \
                self._ptn_date.match(tag.string)

    def get_link(self, link):
        return link

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
        if html.find('<title>One Bryant Park Photos') > -1 or \
                html.find('<title>One Bryant Park - Photo') > -1:
            return self._filter_html('')

        start = html.find('<div class="panel-pane pane-node-body" >')
        if start == -1:
            start = html.find('<div class="panel-pane pane-content-field pane-field-image-file" >')
        if start == -1:
            start = html.find('<div class="panel-pane pane-content-field pane-field-video-player" >')
        if start == -1:
            start = html.index('<!-- /#bw-above_content-left-->')
        
        end = html.find('Contact:          </h2>', start)
        if end == -1:
            end = html.find('<div id="bw-sidebar-right" class="bw-sidebar">', start)
        if end == -1:
            end = html.index('<!-- Enterprise Site Footer Section -->', start)
        
        html = html[start:end]
        return self._filter_html(html)
