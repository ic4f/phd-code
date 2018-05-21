import datetime
import os
import sys
import re
from shared import config
from shared.database import DbTool
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from data.matches import MatchLoader
from data.tokens import TokenLoader
from data.scores import ScoreLoader

MATCHES_NAME = 'final'


class DbLoader(object):

    def __init__(self):
        self._db = DbTool()
        self._br = ConfigReader().get('MARKER_BR')

    def run(self):
        self._db.open()       
        for company_id in range(1, 2):
            print 'Processing company {0}'.format(company_id)
            self._process(company_id)
        self._db.commit()
        self._db.close()

    def _process(self, company_id):
        matchloader = MatchLoader(company_id, MATCHES_NAME)
        tokens = TokenLoader(company_id)
        releases = ReleaseLoader(company_id).get_releases()
        articles = ArticleLoader(company_id).get_articles()
        scores = ScoreLoader(company_id)

        for release_id in matcheloader.get_release_ids():
            release = releases[release_id]
            rel_tokens = tokens.get_stripped_release_token_block(release_id, 0, sys.maxint)

    def _write_doc(self, pub, date, headline, byline, body):
        pub = pub.strip()
        date = date.strip()
        byline = byline.strip()
        headline = headline.strip()
        body = ''.join(body)

        if pub in self._pub_dic:
            pub_id = self._pub_dic[pub]
        else:
            pub_id = self._db.create_pub(pub)
            self._db.commit()
            self._pub_dic[pub] = pub_id

        art_id = self._db.create_article(self._company_id, pub_id, date, byline, headline, body)
