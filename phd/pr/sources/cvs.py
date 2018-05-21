import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Cvs(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\d\d)\.(\d\d)\.(201\d)$')

    def get_linkpages(self):
        all_html = []
        base = 'http://info.cvscaremark.com/newsroom/press-releases?page='
        for i in range(0, 8):
            url = base + str(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('<td colspan="2" class="view-label">2012<td>')
            end = html.index('<div class="press-release-container">', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'td' and \
                tag.parent.has_key('class') and \
                tag.parent.get('class')[0] == 'views-field' and \
                tag.parent.get('class')[1] == 'views-field-title'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and \
                tag.get('class')[0] == 'date-display-single'

    def get_link(self, link):
        return urljoin('http://info.cvscaremark.com/', link)

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
        year = int(match.group(3))
        month = int(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<h5>')
        end = html.find('<p>SOURCE', start)
        if end == -1:
            end = html.index('<a href="/newsroom/press-releases" class="back" >', start)
        html = html[start:end]
        return self._filter_html(html)
