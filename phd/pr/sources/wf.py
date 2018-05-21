import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Wf(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+&#160;)(\d{1,2})')
        self._ptn_date2 = re.compile('(\w+)[^\d]+(\d{1,2})')

    def get_linkpages(self):
        all_html = []
        url = 'https://www.wellsfargo.com/press/?year=2012'
        html = urlopen(url).read()
        start = html.index('<table cellspacing="0" id="pressLayout">')
        end = html.index('!--  end contentLeft -->', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') 

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'td' and tag.has_key('class') and \
                tag.get('class')[0] == 'lftCol'

    def get_link(self, link):
        if link.find('.pdf') == -1:
            return urljoin('https://www.wellsfargo.com/', link)
        else:
            return None

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s.strip())
        return ''.join(sb)

    def get_date(self, tag):
        sb = []
        raw = tag.stripped_strings.next()
        raw = raw.strip()
        match = self._ptn_date2.match(raw)
        if not match:
            print raw
            raise Exception('date format did not match pattern')
        year = 2012
        month = common.get_month_by_name(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<article>')
        end = html.index('<footer>', start)
        html = html[start:end]
        return self._filter_html(html)
