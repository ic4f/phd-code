import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Deere(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\d\d) (\w+) (20\d\d)')

    def get_linkpages(self):
        all_html = []
        base = 'http://search.deere.com/DDC/en_US/News/?v%3afile=viv_1zWd6J&v:state=root|root-{0}-10|0&'
        for i in range(0, 81, 10):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('id="deere-results"')
            end = html.index('</ol><div id="search-details"', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class') and tag.get('class')[0] == 'title'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and \
                tag.get('class')[0] == 'value' and \
                tag.parent.name == 'div' and tag.parent.has_key('class') and \
                tag.parent.get('class')[0] == 'field' and \
                tag.parent.get('class')[1] == 'field-datefield' and \
                self._ptn_date.match(tag.string.strip())

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
        year = int(match.group(3))
        month = common.get_month_by_name(match.group(2))
        day = int(match.group(1))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<div class="MOD_GC_3">')
        end = html.index('<div class="ls-area" id="jdofl-en-us-col-1-row-3-area-1">', start)
        html = html[start:end]
        return self._filter_html(html)
