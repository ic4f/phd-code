import sys
from operator import itemgetter
from difflib import SequenceMatcher
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from data.tokens import TokenLoader
from data.matches import MatchMaker
from data.blocks import BlockLoader
from data.duplicates import DuplicateLoader


class MatchFinder(object):
    
    def __init__(self, company_id, release_ids, article_ids, required_length, min_length, blocks_name_toignore):
        self._company_id = company_id
        self._release_ids = release_ids
        self._article_ids = article_ids
        self._required_length = required_length
        self._min_length = min_length
        
        self._tokens = TokenLoader(company_id)
        
        self._releases = ReleaseLoader(company_id).get_releases()
        self._articles = ArticleLoader(company_id).get_articles()
        
        self._ignoreblocks = BlockLoader(company_id, blocks_name_toignore).get_blocks()
        self._count_ignore = 0

        dloader = DuplicateLoader(company_id)
        self._rel_duplicates = dloader.get_release_duplicates()
        self._art_duplicates = dloader.get_article_duplicates()


    def find_matches(self, output_name):       
        matchmaker = MatchMaker(self._company_id, output_name)
        matcher = SequenceMatcher(autojunk=False)        
        message = 'Processing company {0}: release {1} of {2}; article {3} of {4}'
        pairs_counter = 0

        for i, release_id in enumerate(self._release_ids): #loop through releases

            if release_id in self._rel_duplicates:
                continue

            matcher.set_seq2(self._tokens.get_release_tokens(release_id, True))
            release_date = self._releases[release_id].date()

            for j, article_id in enumerate(self._article_ids): #loop through articles 
               
                if article_id in self._art_duplicates:
                    continue

                if j % 100 == 0:
                    print message.format(self._company_id, i+1, len(self._release_ids), j+1, len(self._article_ids))

                matcher.set_seq1(self._tokens.get_article_tokens(article_id, True))
                article_date = self._articles[article_id].date()

                if article_date >= release_date: #search for matches if article appeared after the release

                    blocks = matcher.get_matching_blocks() #block form: (i,j,k) where i = article (seq1), j = release (seq2)
                    if len(blocks) > 0: #if there are blocks

                        valid_blocks = self._get_blocks(blocks, release_id, article_id)
                        if len(valid_blocks) > 0: #if there are valid blocks

                            matchmaker.add_blocks(release_id, article_id, valid_blocks)
                            print '\tfound match for release={0} and article={1}'.format(release_id, article_id)
                            pairs_counter += 1

        print 'total matching pairs: {0}'.format(pairs_counter)
        print 'ignored bad discriminators: {0}'.format(self._count_ignore)
        matchmaker.save()


    def _get_blocks(self, blocks, release_id, article_id): 
        blocklist = []
        required_length_check = False
        
        for b in blocks:
            i = b[0]
            j = b[1]
            k = b[2]

            rel_match = self._tokens.get_stripped_release_token_block(release_id, j,j+k)
            art_match = self._tokens.get_stripped_article_token_block(article_id, i,i+k)

            rel_temp = ' '.join(rel_match)
            art_temp = ' '.join(art_match)

            if rel_temp.lower() != art_temp.lower():
                print rel_temp.lower()
                print art_temp.lower()
                raise Exception("blocks don't match")           

            #check against bad discriminators BEFORE updating required_length_check
            if rel_temp.lower() in self._ignoreblocks:
                self._count_ignore += 1
                continue

            #check for min_length BEFORE updating required_length_check
            if len(rel_match) < self._min_length:
                continue

            if len(rel_match) >= self._required_length:
                required_length_check = True

            blocklist.append(b)

        #sort by length, decending
        if len(blocklist) == 0:
            return []

        if not required_length_check:
            return []
        else:
            blocklist = sorted(blocklist, key=itemgetter(2), reverse=True)     
            return blocklist
