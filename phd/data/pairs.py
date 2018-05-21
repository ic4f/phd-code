import os
import string
from shared import common


class PairLoader(object):

    def __init__(self, company_id, pairs_name):
        self._load(company_id, pairs_name)

    def get_pairs(self):
        return self._pairs

    def has_pair(self, release_id, article_id):
        tpl = release_id, article_id
        return tpl in self._pairs
    
    def _load(self, company_id, pairs_name):        
        self._pairs = []
        dir_path = common.get_pairs_path(pairs_name)
        path = os.path.join(dir_path, str(company_id))
        with open(path) as f:
            lines = [line.strip() for line in f.readlines()]
            for line in lines:
                tmp = line.split('-')
                pair = int(tmp[0]), int(tmp[1])
                self._pairs.append(pair)
