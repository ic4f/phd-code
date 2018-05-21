import datetime
import re
from urlparse import urljoin
from urllib import urlopen
import nltk
from base_source import BaseSource
from shared import common


class Liberty(BaseSource):

    def __init__(self):
        self._ptn_date = re.compile('^(\w+) (\d\d), 2012$')
        self._ptn_link = re.compile('.*cid=(\d{13})')

    def get_linkpages(self):
        all_html = []
        url = 'http://www.libertymutualgroup.com/omapps/ContentServer?fid=1142008723439&ln=en&pagename=LMGroup%2FViews%2FLMG&ft=9&type=pr&cid=1142008723439&yr=2012'
        html = urlopen(url).read()
        start = html.index('<h4>')
        end = html.index('side_column', start)
        html = html[start:end]
        all_html.append(html)
        return all_html

    def is_link(self, tag):     
        return tag.has_key('href') and tag.has_key('class') and \
                (tag.get('class')[0] == 'more' or tag.get('class')[0] == 'pdf')

    def is_title(self, tag):
        return tag.name == 'h4' and tag.string is not None
    
    def is_date(self, tag):
        return tag.name == 'strong' and tag.string is not None and \
            self._ptn_date.match(tag.string)

    def get_link(self, link):
        base = 'http://www.libertymutualgroup.com/omapps/ContentServer?kw=true&c=cms_asset&pagename=LMGroup%2FViews%2FlmgView98&cid={0}'
        match = self._ptn_link.match(link)
        cid = match.group(1)
        return base.format(cid)

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
        return "utf-8"

    def get_text(self, html):
        start = html.index('<em>Keywords</em>')
        end = html.find('<strong>Contact:', start)
        if end == -1:
            end = html.find('Press Contact:', start)
        if end == -1:
            end = html.index('</body>', start)
        html = html[start:end]
        return self._filter_html(html)
