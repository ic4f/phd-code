import cPickle
import string
from shared import common


class MatchMaker(object):

    def __init__(self, company_id, matches_name):
       self._company_id = company_id
       self._matches_name = matches_name
       self._r_a_blocks = {}

    def add_blocks(self, release_id, article_id, blocks):
        if not release_id in self._r_a_blocks:
            a_blocks = {}
            self._r_a_blocks[release_id] = a_blocks            
        else:
            a_blocks = self._r_a_blocks[release_id]
        a_blocks[article_id] = blocks

    def save(self):
        path = common.get_pickled_matches_path(self._company_id, self._matches_name)
        with open(path, 'wb') as f:
            cPickle.dump(self._r_a_blocks, f, -1)


class MatchLoader(object):

    def __init__(self, company_id, matches_name):
        self._load(company_id, matches_name)

    def count_rel_art_pairs(self):
        count = 0
        for release_id in self._rel_art_blocks:
            art_blocks = self._rel_art_blocks[release_id]
            count += len(art_blocks)
        return count

    def count_matching_blocks(self):
        count = 0
        for release_id in self._rel_art_blocks:
            art_blocks = self._rel_art_blocks[release_id]
            for article_id in art_blocks:
                block = art_blocks[article_id]
                count += len(block)
        return count

    def get_release_ids(self):
        ids = set()
        for release_id in self._rel_art_blocks:
            ids.add(release_id)
        return ids

    def get_article_ids(self, release_id=None):
        ids = set()
        if release_id is None: #loop through all releases
            for release_id in self._rel_art_blocks:
                self._get_article_ids_helper(release_id, ids)
        else: #use only one release
            self._get_article_ids_helper(release_id, ids)
        return ids

    def _get_article_ids_helper(self, release_id, ids):
        art_blocks = self._rel_art_blocks[release_id]
        for article_id in art_blocks:
            ids.add(article_id)            

    def get_matches(self, release_id, article_id):
        art_blocks = self._rel_art_blocks[release_id]
        return art_blocks[article_id]

    def _load(self, company_id, matches_name):
        pickle_path = common.get_pickled_matches_path(company_id, matches_name)
        with open(pickle_path, 'rb') as f:
            self._rel_art_blocks = cPickle.load(f)
