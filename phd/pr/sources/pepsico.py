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


class Pepsico(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\d{1,2})/(\d{1,2})/2012 -')

    def get_linkpages(self):
        all_html = []
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('PR_SOURCES')
        path2 = os.path.join(root, path1)
        path = os.path.join(path2, 'pepsico.html')
        print 'collecting links from source file'
        with open(path) as f:
            lines = f.readlines()
            all_html.append(''.join(lines))
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.string is not None

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'h5'

    def get_link(self, link):
        return urljoin('http://www.pepsico.com/', link)

    def get_title(self, tag):
        return tag.string

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern')
        year = 2012
        month = int(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.find('</style>')
        if start == -1:
            start = html.index('<h2 class="content_releaseTitle" style="font-size:10pt">')
        end = html.find('<p>SOURCE', start)
        if end == -1:
            end = html.index('<!-- END Main Content Area -->', start)

        html = html[start:end]
        return self._filter_html(html)
