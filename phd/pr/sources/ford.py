import sys
import os.path
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common
from shared.config import ConfigReader


class Ford(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\d\d) (\w\w\w) 2012')

    def get_linkpages(self):
        all_html = []
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('PR_SOURCES')
        path2 = os.path.join(root, path1)
        path = os.path.join(path2, 'ford.html')
        print 'collecting links from source file'
        with open(path) as f:
            lines = f.readlines()
            all_html.append(''.join(lines))
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href')

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and \
                tag.get('class')[0] == 'feeds-date' and \
                self._ptn_date.match(tag.string)

    def get_link(self, link):        
        link = '{0}?view=print'.format(link)
        return urljoin('http://corporate.ford.com/', link)

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s.strip())
        return ''.join(sb)

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern')
        year = 2012
        month = common.get_month_by_name(match.group(2))
        day = int(match.group(1))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<div class="hub-feature-body">')
        end = html.index('<!--hub-feature-body -->', start)
        html = html[start:end]
        return self._filter_html(html)
