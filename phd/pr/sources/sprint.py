import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Sprint(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\d\d) (\w+) (\d\d\d\d)')

    def get_linkpages(self):
        all_html = []
        url = 'http://newsroom.sprint.com/section_display.cfm?archiveYear=2012&section_id=1'
        print 'collecting links from {0}'.format(url)
        html = urlopen(url).read()
        start = html.index('archiveNav')
        end = html.index('END center', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'h2'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and \
            tag.get('class') is not None and tag.get('class')[0] == "strDate"

    def get_link(self, link):
        url = urljoin('http://newsroom.sprint.com/', link)
        if url.startswith('http://newsroom.sprint.com/article'):
            return url.replace('display', 'print')
        else:
            return url.replace('.htm', '.print')

    def get_title(self, tag):
        return tag.string

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern')
        year = int(match.group(3))
        month = common.get_month_by_name(match.group(2))
        day = int(match.group(1))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('</h3>')
        end = html.index('</body>', start)
        html = html[start:end]
        return self._filter_html(html)
