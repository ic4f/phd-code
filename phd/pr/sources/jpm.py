import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Jpm(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w\w\w) (\d{1,2}), 2012')

    def get_linkpages(self):
        all_html = []
        base = 'http://investor.shareholder.com/jpmorganchase/releases.cfm?Year=2012&ReleasesType=Current&PageNum='
        for i in range(1,10):
            url = base + str(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('2012 Current Releases')
            end = html.index('dataTableBottom', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'td' and \
            tag.get('href').startswith('releasedetail')

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'td' and len(tag.contents) == 3 and \
            self._ptn_date.match(tag.contents[2].strip())

    def get_link(self, link):
        return urljoin('http://investor.shareholder.com/jpmorganchase/', link)

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s)
        return ''.join(sb)

    def get_date(self, tag):
        raw = tag.contents[2].strip()
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
        start = html.find('<h3>')
        if start == -1:
            start = html.index('<p>')
        end = html.index('<a href="#" onclick="window.close();', start)
        html = html[start:end]
        return self._filter_html(html)
