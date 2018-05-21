import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Johnson(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w\w\w)\s+(\d{1,2}), 2012$')

    def get_linkpages(self):
        all_html = []
        base = 'http://johnsoncontrols.mediaroom.com/index.php?o={0}&s=news_releases&year=2012'
        for i in range(0, 76, 25):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('2012 Archives')
            end = html.index('table_footer', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class') and tag.get('class')[0] == 'itemlink'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'div' and tag.has_key('class') and \
                tag.get('class')[0] == 'item_date' and \
                self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return '{0}&printable'.format(link)

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s)
        return ''.join(sb)

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern: {0}'.format(raw))
        year = 2012
        month = common.get_month_by_name(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<div class="wd_news_releases-detail">')

        end = html.find('<p>SOURCE ', start)
        if end == -1:
            end = html.find('<p>Contact:', start)
        if end == -1:
            end = html.find('<p>CONTACT', start)
        if end == -1:
            end = html.index('<!-- ITEMDATE:', start)

        html = html[start:end]
        return self._filter_html(html)
