import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource


class Allstate(BaseSource):
    def __init__(self):
        self._ptn_date = re.compile('(\d\d)/(\d\d)/(\d\d\d\d)')

    def get_linkpages(self):
        all_html = []
        base = "http://www.allstatenewsroom.com/channels/News-Releases/releases?page="
        for i in range(1,7):
            url = base + str(i)
            print 'collecting links from {0}'.format(url)
            all_html.append(urlopen(url).read())
        return all_html

    def is_link(self, tag):
        return tag.name == 'a' and \
            tag.string is not None and tag.string.startswith("read more")

    def is_title(self, tag):
        return tag.name == 'a' and \
            tag.get('class') is not None and tag.get('class')[0] == "title"

    def is_date(self, tag):
        return tag.name == 'span' and \
            tag.get('class') is not None and tag.get('class')[0] == "pubDate"

    def get_link(self, link):
        return urljoin("http://www.allstatenewsroom.com", link) + "?mode=print"

    def get_title(self, tag):
        return tag.string

    def get_date(self, tag):
        raw = tag.string.strip()
        match = self._ptn_date.match(raw)
        if not match:
            raise Exception('date format did not match pattern')
        year = int(match.group(3))
        month = int(match.group(1))
        day = int(match.group(2))
        return datetime.date(year, month, day)
    
    def get_encoding(self):
        return "utf-8"

    def get_text(self, html):
        start = html.index('<p>')

        end = html.find('###', start)
        if end == -1:
            end = html.find('<p>Contact:', start)
        if end == -1:
            end = html.find('<strong>Contact:', start)
        if end == -1:
            end = html.index('</html>', start)
        html = html[start:end]
        return self._filter_html(html)
