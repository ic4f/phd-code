import os
import string
from shared import common


class DuplicateLoader(object):

    def __init__(self, company_id):
        self._load(company_id)

    def get_release_duplicates(self):
        return self._rel_dups
    
    def get_article_duplicates(self):
        return self._art_dups

    def _load(self, company_id):        
        path_rel = common.get_rel_duplicates_path(company_id)
        path_art = common.get_art_duplicates_path(company_id)
        self._rel_dups = self._load_dups(path_rel)       
        self._art_dups = self._load_dups(path_art)

    def _load_dups(self, path):        
        if not os.path.exists(path):
            return []
        else:
            with open(path) as f:
                dups = [int(line.strip()) for line in f.readlines()]
            return dups
