import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Merck(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\d{1,2})/(\d{1,2})/(1\d) ')

    def get_linkpages(self):
        all_html = []
        url = 'http://www.mercknewsroom.com/news-releases'
        html = urlopen(url).read()
        start = html.index('view-content')
        end = html.index('<div id="content-tab-3" class="tabs-content">', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'span' and \
            tag.parent.has_key('class') and tag.parent.get('class')[0] == 'field-content' and \
            tag.parent.parent.name == 'div' and \
            tag.parent.parent.has_key('class') and tag.parent.parent.get('class')[0] == 'views-field-item' and \
            tag.parent.parent.get('class')[1] == 'views-field-title'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and \
                tag.get('class')[0] == 'field-content' and \
                tag.parent.name == 'div' and tag.parent.has_key('class') and \
                tag.parent.get('class')[1] == 'views-field-created' and \
                self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return urljoin('http://www.mercknewsroom.com/', link)

    def get_title(self, tag):
        return tag.string

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
        start = html.index('<div class="panel-pane pane-node-body" >')
        end = html.find('Contact:          </h2>', start)
        if end == -1:
            end = html.index('<div class="bw-sidebar">', start)
        html = html[start:end]
        return self._filter_html(html)
