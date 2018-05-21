import os.path
import cPickle
from shared import common 
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from shared.tokenizer import Tokenizer
from shared.config import ConfigReader 


class TokenWriter(object):

    def write_tokens(self, company_id):
        tokenizer = Tokenizer()
        br = ConfigReader().get('MARKER_BR')

# uncomment this block when done with press releases
#        dic = {}
#        articles = ArticleLoader(company_id).get_articles()
#        for i, key in enumerate(articles):
#            if i % 50 == 0:
#                print 'pickling article {0} of {1} for company {2}'.format(i+1, len(articles), company_id)
#            article = articles[key]
#            text = article.headline() + '\n\n' + article.body()
#            self._add_tokens_to_dic(tokenizer, dic, article.id(), text, br)
#
#        output_path = common.get_pickled_news_tokens_path(company_id)
#        self._pickle(company_id, dic, output_path)

        dic = {}
        releases = ReleaseLoader(company_id).get_releases()
        for i, key in enumerate(releases):
            if i % 50 == 0:
                print 'pickling release {0} of {1} for company {2}'.format(i+1, len(releases), company_id)
            release = releases[key]
            text = release.title() + '\n\n' + release.body()
            self._add_tokens_to_dic(tokenizer, dic, release.id(), text, br)

        output_path = common.get_pickled_pr_tokens_path(company_id)
        self._pickle(company_id, dic, output_path)

    def _add_tokens_to_dic(self, tokenizer, dic, id, text, br):
        text = text.replace('\n', ' {0} '.format(br))
        tokens = tokenizer.get_tokens(text)
        dic[id] = tokens

    def _pickle(self, company_id, dic, output_path):
        with open(output_path, 'wb') as f:
            cPickle.dump(dic, f, -1)

