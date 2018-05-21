import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Metlife(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+)\s+(\d\d), 2012$')

    def get_linkpages(self):
        all_html = []
        url = 'https://www.metlife.com/about/press-room/us-press-releases/2012/index.html?WT.ac=PRO_PRO_PR-archives2013_5-91481_T6934-AB-us-press-releases&oc_id=PRO_PRO_PR-archives2013_5-91481_T6934-AB-us-press-releases'
        html = urlopen(url).read()
        start = html.index('Press Release List Container')
        end = html.index('<!--Press Release List Inner Content: End-->', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):        
        return tag.has_key('href') and tag.parent.name == 'div' and \
            tag.parent.has_key('class') and tag.parent.get('class')[0] == 'content'

    def is_title(self, tag):
        return self.is_link(tag)

    def is_date(self, tag):
        return tag.name == 'label' and tag.string is not None and \
            self._ptn_date.match(tag.string.strip())

    def get_link(self, link):
        return urljoin('https://www.metlife.com/about/press-room/us-press-releases/2012/', link)

    def get_title(self, tag):
        if str(type(tag.contents[0])) != "<class 'bs4.element.NavigableString'>":
            span = tag.contents[0]
            return span.contents[1]
        else:
            sb = []
            for s in tag.stripped_strings:
                sb.append(s)
            return ' '.join(sb)

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
        start = html.index('<div id="prsFlSectionContent">')
        end = html.index('<p>Contact:</p>', start)
        html = html[start:end]
        return self._filter_html(html)

