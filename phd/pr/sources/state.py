import datetime
import os.path
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common
from shared.config import ConfigReader


class State(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d{1,2}), 2012$')

    def get_linkpages(self):
        all_html = []
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('PR_SOURCES')
        path2 = os.path.join(root, path1)
        path = os.path.join(path2, 'state.html')
        print 'collecting links from source file'
        with open(path) as f:
            lines = f.readlines()
            all_html.append(''.join(lines))
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class') and \
                tag.get('class')[0] == 'date-link' 

    def is_title(self, tag):
        return tag.name == 'p' and tag.has_key('class') and tag.get('class')[0] == 'title'

    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and tag.get('class')[0] == 'pub-date'

    def get_link(self, link):
        return link

    def get_title(self, tag):
        return tag.string

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
        return "latin-1"

    def get_text(self, html):
        start = html.find('<h1 id="headline">')
        if start == -1:
            start = html.index("<section class='group' id='main_left'>")

        end = html.find("<!-- left column-->", start)
        if end == -1:
            end = html.index("</section>", start)

        html = html[start:end]
        return self._filter_html(html)
