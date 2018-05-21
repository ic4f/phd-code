import sys
import hashlib
from shared import common
from data.articles import ArticleLoader
from data.releases import ReleaseLoader


class DuplicateFinder(object):

    def __init__(self, company_id):
        self._company_id = company_id

    def find_release_duplicates(self):
        hashes = self._load_rel_hashes()
        dups = self._get_duplicates(hashes)
        if len(dups) > 0:
            for d in dups:
                print d

    #Quick 'n dirty solution: print to file since I know there are duplicates. 
    #   Run once and change permissions on output directory.
    def find_article_duplicates(self):
        hashes = self._load_art_hashes()
        dups = self._get_duplicates(hashes)
        if len(dups) > 0:
            path = common.get_art_duplicates_path(self._company_id)
            with open(path, 'w') as f:
                for d in dups:
                    f.write('{0}\n'.format(d))

    def _get_duplicates(self, hashes):
        dups = set()
        hashset = set()
        for id in hashes:
            if hashes[id] in hashset:
                dups.add(id)
            else:
                hashset.add(hashes[id])
        return dups

    def _load_rel_hashes(self):
        hashes = {}
        releases = ReleaseLoader(self._company_id).get_releases()
        for release_id in releases:
            release = releases[release_id]
            text = str(release.date()) + release.title() + release.body() 
            m = hashlib.md5()
            m.update(text)
            hashes[release_id] = m.hexdigest()
        return hashes

    def _load_art_hashes(self):
        hashes = {}
        articles = ArticleLoader(self._company_id).get_articles()
        for article_id in articles:
            article = articles[article_id]
            text = str(article.date()) + article.pub() + article.headline() + article.body()
            m = hashlib.md5()
            m.update(text)
            hashes[article_id] = m.hexdigest()
        return hashes
