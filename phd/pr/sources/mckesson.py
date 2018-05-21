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


class Mckesson(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d\d), (201\d)$')

    def get_linkpages(self):
        all_html = []
        url = 'http://www.mckesson.com/en_us/McKesson.com/About%2BUs/Newsroom/Press%2BReleases%2BArchives/2012/2012.html'
        print 'collecting links from {0}'.format(url)
        html = urlopen(url).read()
        start = html.index('<div id="articleList">')
        end = html.index('articleDivClone', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent is not None and \
            tag.parent.name == 'strong'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'strong' and tag.string is not None and \
            self._ptn_date.match(tag.string)

    def get_link(self, link):
        return urljoin('http://www.mckesson.com/', link)

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
        month = common.get_month_by_name(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<!-- PRESS_KIT INCLUDE END-->')
        end = html.find('PR Contact', start)
        if end == -1:
            end = html.index('<!-- main table section ends -->', start)
        html = html[start:end]
        return self._filter_html(html)
