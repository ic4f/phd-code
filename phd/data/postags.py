import cPickle
import os.path
import string
from shared import common
from shared.config import ConfigReader


class POSTagLoader(object):

    def __init__(self, company_id, name):
        self._load_dictionaries(company_id, name)

    def get_release_tags(self, release_id):
        return self._rel_tags[release_id]
    
    def get_article_tags(self, article_id):
        return self._art_tags[article_id]

    def _load_dictionaries(self, company_id, name):
        filename = '{0}.pickle'.format(company_id)
        
        path1 = common.get_postags_path()
        path2 = os.path.join(path1, name)
        
        path = os.path.join(path2, common.DOCTYPE_PR)        
        filepath = os.path.join(path, filename)
        with open(filepath, 'rb') as f:
            self._rel_tags = cPickle.load(f)
        
        path = os.path.join(path2, common.DOCTYPE_NEWS)        
        filepath = os.path.join(path, filename)
        with open(filepath, 'rb') as f:
            self._art_tags = cPickle.load(f)
