import sys
import sys
import os.path
import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common
from shared.config import ConfigReader


class Citi(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\d\d) (\w\w\w)')

    def get_linkpages(self):
        all_html = []
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('PR_SOURCES')
        path2 = os.path.join(root, path1)
        path = os.path.join(path2, 'citi.html')
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
        return tag.name == 'div' and tag.has_key('class') and \
                tag.get('class')[0] == 'info' and \
                self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return link

    def get_title(self, tag):
        sb = []
        for s in tag.stripped_strings:
            sb.append(s.strip())
        return ' '.join(sb)

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
        start = html.index('<div class="article_body">')
        end = html.index('<div class="rightbar_wrap">', start)
        html = html[start:end]
        return self._filter_html(html)
