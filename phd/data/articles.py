import os.path
import datetime
from shared import common
from shared.config import ConfigReader


class ArticleLoader(object):

    def __init__(self, company_id):
        self._news = {}
        self._load(company_id)

    def get_articles(self):
        return self._news

    def _load(self, company_id):
        cfr = ConfigReader()
        p1 = cfr.get('ROOT_ORIGINAL')
        p2 = cfr.get('FORMATTED_NEWS')
        p3 = os.path.join(p1, p2)
        metafile = common.get_list_file_name(company_id)

        path_text = os.path.join(p3, str(company_id))
        path_meta = os.path.join(p3, metafile)

        news_text = self._load_text(path_text)
        self._load_meta(path_meta, news_text)

    def _load_text(self, path):
        text = {}
        article_id = -1
        sb = []
        with open(path) as f:
            while True:
                line = f.readline()
                if line == '':
                    text[article_id] = ''.join(sb) #flush last record
                    break
                if line.startswith('LOTW-ID: '):
                    if article_id != -1:
                        text[article_id] = ''.join(sb)
                    article_id = int(line[9:].strip())
                    sb = []
                else:
                    sb.append(line)
        return text

    def _load_meta(self, path, news_text):
        article_id = -1
        with open(path) as f:
            while True:
                line = f.readline()
                if line == '':
                    self._news[article_id] = Article(article_id, pub, date, headline, byline, news_text[article_id])
                    break
                if line.startswith('LOTW-ID: '):
                    if article_id != -1:
                        self._news[article_id] = Article(article_id, pub, date, headline, byline, news_text[article_id])
                    article_id = int(line[9:].strip())
                elif line.startswith('LOTW-PUB: '):
                    pub = line[10:]
                elif line.startswith('LOTW-DATE: '):
                    date = line[11:]
                elif line.startswith('LOTW-HEADLINE: '):
                    headline = line[15:]
                elif line.startswith('LOTW-BYLINE: '):
                    byline = line[13:]


class Article(object):

    def __init__(self, article_id, pub, date, headline, byline, body):
        self._news = article_id, pub, self._load_date(date), headline, byline, body
    
    def id(self):
        return self._news[0]

    def pub(self):
        return self._news[1]

    def date(self):
        return self._news[2]

    def headline(self):
        return self._news[3]
                
    def byline(self):
        return self._news[4]
                
    def body(self):
        return self._news[5]

    def _load_date(self, date):
        date = date.strip()
        return datetime.datetime.strptime(date, '%Y-%m-%d') 
