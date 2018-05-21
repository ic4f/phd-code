import cPickle
import string
from shared import common
from shared.config import ConfigReader


class TokenLoader(object):

    def __init__(self, company_id):
        self._load_dictionaries(company_id)
        self._exclude_tokens = set(string.punctuation)
        self._exclude_tokens.add(ConfigReader().get('MARKER_BR'))

    def get_release_tokens(self, release_id, lowercase):
        tokens = self._pr_tokens[release_id]
        if lowercase:
            tokens = [t.lower() for t in tokens]
        return tokens
    
    def get_article_tokens(self, article_id, lowercase):
        tokens = self._news_tokens[article_id]
        if lowercase:
            tokens = [t.lower() for t in tokens]
        return tokens

    def get_stripped_release_token_block(self, release_id, start, length):
        return self._strip_tokens(self._pr_tokens[release_id], start, length)

    def get_stripped_article_token_block(self, article_id, start, length):
        return self._strip_tokens(self._news_tokens[article_id], start, length)

    def _strip_tokens(self, tokens, start, end):
        token_list = tokens[start:end] 
        return [t for t in token_list if t not in self._exclude_tokens]

    def _load_dictionaries(self, company_id):
        path = common.get_pickled_news_tokens_path(company_id)
        with open(path, 'rb') as f:
            self._news_tokens = cPickle.load(f)
        
        path = common.get_pickled_pr_tokens_path(company_id)
        with open(path, 'rb') as f:
            self._pr_tokens = cPickle.load(f)
