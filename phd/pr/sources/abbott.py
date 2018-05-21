import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Abbott(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d{1,2})')

    def get_linkpages(self):
        all_html = []
        base = 'http://www.abbott.com/global/url/pressReleases/en_US/60.5:5/general_content/Press_Release_Selector_01.htm?page={0}&year=2012'
        for i in range(0,3):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('<tr class="press-release">')
            end = html.index('bottom pagination', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'td' and \
            tag.parent.has_key('class') and tag.parent.get('class')[0] == 'description'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'p' and tag.parent.name == 'td' and \
                tag.parent.has_key('class') and \
                tag.parent.get('class')[0] == 'date' and \
                self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return urljoin('http://www.abbott.com/', link)

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
        start = html.index('<div id="press-release-lower-content"')
        end = html.index('<div class="prcontact hr-stamp">', start)
        html = html[start:end]
        return self._filter_html(html)
