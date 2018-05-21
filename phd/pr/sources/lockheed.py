import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource


class Lockheed(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d\d), (2012)$')
        self._ptn_link1 = re.compile('/us/news/press-releases/2012/\w+/')
        self._ptn_link2 = re.compile('/uk/news/press-releases/2012-press-releases')
        self._ptn_link3 = re.compile('/us/aeronautics/media-center/aero-press-releases')

    def get_linkpages(self):
        all_html = []
        url = "http://www.lockheedmartin.com/us/news/press-releases/2012.html"
        all_html.append(urlopen(url).read())
        return all_html

    def is_link(self, tag):
        return 'href' in tag.attrs and \
            (self._ptn_link1.match(tag.get('href')) or \
            self._ptn_link2.match(tag.get('href')) or \
            self._ptn_link3.match(tag.get('href')))

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'li' and tag.string is not None and \
            self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return urljoin('http://www.lockheedmartin.com/us/news/press-releases/', link)

    def get_title(self, tag):
        return tag.string

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
        start = html.index('<div class="text parbase section">')
        end = html.index('<!-- /centerCol -->', start)
        html = html[start:end]
        return self._filter_html(html)
