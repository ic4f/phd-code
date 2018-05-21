import sys
import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Unitedcont(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\d{1,2})\.(\d{1,2})\.(1\d)')

    def get_linkpages(self):
        all_html = []
        url = 'http://ir.unitedcontinentalholdings.com/phoenix.zhtml?c=83680&p=irol-mediacenterpressreleases'
        all_html.append(urlopen(url).read())
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.has_key('class') and tag.get('class')[0] == 'title'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'span' and tag.has_key('class') and tag.get('class')[0] == 'date'

    def get_link(self, link):
        text = urljoin('http://ir.unitedcontinentalholdings.com/', link)
        text = text.replace('newsArticle', 'newsArticle_print')
        return text

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
        year = 2000 + int(match.group(3))
        month = int(match.group(1)) 
        day = int(match.group(2))
        return datetime.date(year, month, day)

    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<span class="ccbnTtl">')
        end = html.find('<p>SOURCE ', start)
        if end == -1:
            end = html.index('</body>', start)
        html = html[start:end]
        return self._filter_html(html)
