import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Delta(BaseSource):
    def __init__(self):
        self._ptn_date2 = re.compile('(\w\w\w) (\d{1,2}), 2012')
        pass

    def get_linkpages(self):
        all_html = []
        base = 'http://news.delta.com/index.php?o={0}&s=43&year=2012'
        for i in range(0, 126, 25):
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
        return self.is_link(tag) #some dates not available on page

    def get_link(self, link):
        return link

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s)
        return ''.join(sb)

    def get_date(self, tag):
        return None

    def get_date_from_body(self, body):
        match = self._ptn_date2.match(body)
        if not match:
            print body
            raise Exception('date format did not match pattern')
        year = 2012
        month = common.get_month_by_name(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<p class="release_data">')
        end = html.find('<p>SOURCE ', start)
        if end == -1:
            end = html.find('<p class="detail_contact">', start)
        if end == -1:
            end = html.index('<div class="wd_page_toolbar">', start)

        html = html[start:end]
        return self._filter_html(html)
