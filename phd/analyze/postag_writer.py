import sys
import cPickle
import os.path
import nltk
from data.matches import MatchLoader
from data.tokens import TokenLoader
from shared.config import ConfigReader 
from shared import common


#POS-tags releases and articles for a given macthes set and stores as pickles
class POSTagWriter(object):
    
    def __init__(self):
        self._br = ConfigReader().get('MARKER_BR')

    def write_tags(self, matches_name, company_id):   
        dic_rel = {}
        dic_art = {}

        matches = MatchLoader(company_id, matches_name)
        tokens = TokenLoader(company_id)       

        rel_ids = matches.get_release_ids()
        for count, release_id in enumerate(rel_ids):
            print 'processing release #{0} of {1}'.format(count+1, len(rel_ids))
            tmp = tokens.get_release_tokens(release_id, False)
            self._process_tokens(tmp, dic_rel, release_id)

        art_ids = matches.get_article_ids()
        for count, article_id in enumerate(art_ids):
            print 'processing article #{0} of {1}'.format(count+1, len(art_ids))
            tmp = tokens.get_article_tokens(article_id, False)
            self._process_tokens(tmp, dic_art, article_id)

        path1 = common.get_postags_path()
        path2 = os.path.join(path1, matches_name)

        path = os.path.join(path2, common.DOCTYPE_PR)
        self._pickle(company_id, dic_rel, path)

        path = os.path.join(path2, common.DOCTYPE_NEWS)
        self._pickle(company_id, dic_art, path)

    def _process_tokens(self, tmp, dic, doc_id):
            tokens = ['\n' if t == self._br else t for t in tmp]
            tagged = nltk.pos_tag(tokens)
            dic[doc_id] = tagged

    def _pickle(self, company_id, dic, path):
        filename = '{0}.pickle'.format(company_id)
        filepath = os.path.join(path, filename)
        with open(filepath, 'wb') as f:
            cPickle.dump(dic, f, -1)

