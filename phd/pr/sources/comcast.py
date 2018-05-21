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


class Comcast(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d{1,2}), 2012$')

    def get_linkpages(self):
        all_html = []
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('PR_SOURCES')
        path2 = os.path.join(root, path1)
        path = os.path.join(path2, 'comcast.html')
        print 'collecting links from source file'
        with open(path) as f:
            lines = f.readlines()
            all_html.append(''.join(lines))
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class')

    def is_title(self, tag):
        return tag.name == 'div' and tag.has_key('class') and \
                tag.get('class')[0] == 'content'

    def is_date(self, tag):
        return tag.name == 'div' and tag.has_key('class') and \
                tag.get('class')[0] == 'date' and \
                self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return '{0}?print=1'.format(link)

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
        start = html.find('<h2>')
        if start == -1:
            start = html.index('<p>')
        html = html[start:]
        return self._filter_html(html)
