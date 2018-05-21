import sys
import os.path
import cPickle
from shared.config import ConfigReader 
from shared import common
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from data.tokens import TokenLoader
from data.subsets import SubsetMaker

SUBSET_ALL = 'all'


# writes subsets: 2 dictionary of IDs, one for pr, one for news:
#   key=company_id; value=set(doc IDs)
class SubsetBuilder(object):

    #makes set of all releases and articles, no exclusion criteria
    def build_subset_all(self):
        subset_maker = SubsetMaker()
        for company_id in range(1, 41):
            print 'Processing company {0}'.format(company_id)
            releases = ReleaseLoader(company_id).get_releases()
            for release_id in releases:
                subset_maker.add_release(company_id, release_id)
            
            articles = ArticleLoader(company_id).get_articles()
            for article_id in articles:
                subset_maker.add_article(company_id, article_id)

        subset_maker.save(SUBSET_ALL)
 
    #makes a subset based on minimum block length criteria; takes existing subset as input
    def make_subset(self, matches_name_in, required_length, min_length, subset_name_out):
        subset_maker = SubsetMaker()
        pair_counter = 0

        for company_id in range(1, 41):
            print 'Processing company {0}'.format(company_id)

            tokens = TokenLoader(company_id)
            matches = MatchLoader(company_id, matches_name_in)

            for release_id in matches.get_release_ids():
                for article_id in matches.get_article_ids(release_id):
                    blocks = matches.get_matches(release_id, article_id)
                    blocklist = bfilter.get_blocks(blocks, release_id, article_id)
                    if len(blocklist) > 0: #if there are valid blocks according to this criteria
                        subset_maker
                        pr_set.add(release_id)
                        news_set.add(article_id)
                        pair_counter += 1
        
        print 'Total pairs: {0}'.format(pair_counter)
        subset_maker.save(subset_name_out)

    def _check_blocks(self, blocks, min_block_len):
        for b in blocks:
            length = b[2]
            if length >= min_block_len:
                return True
        return False
