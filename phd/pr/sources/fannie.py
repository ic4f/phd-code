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


class Fannie(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d{1,2}), 2012$')

    def get_linkpages(self):
        all_html = []
        base = 'http://www.fanniemae.com/portal/jsp/filter-media.html?keyword=&topic=all_news_categories&financial_news=all_news_subcategories&year=2012&month=month&pageno={0}'
        for i in range(1,33):
            url = base.format(i)
            print 'collecting links from {0}'.format(url)
            html = urlopen(url).read()
            start = html.index('results_list no_bullets">')
            end = html.index('function searchPageFunction', start)
            html = html[start:end]
            all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'li' 

    def is_title(self, tag):
        return tag.name == 'p' and tag.parent.name == 'a' and \
                len(tag.attrs) == 0 and \
                tag.previous_sibling is not None and \
                tag.previous_sibling.previous_sibling.has_key('class') and \
                tag.previous_sibling.previous_sibling.get('class')[0] == 'date'

    def is_date(self, tag):
        return tag.name == 'p' and tag.has_key('class') and tag.get('class')[0] == 'date' and \
            self._ptn_date.match(tag.string)

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
        year = 2012
        month = common.get_month_by_name(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<h2 class="subhead">')
        end = html.index('<footer>', start)
        html = html[start:end]
        return self._filter_html(html)
