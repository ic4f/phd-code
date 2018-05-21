import sys
from data.tokens import TokenLoader
from data.matches import MatchLoader
from shared.config import ConfigReader 
from shared import common

POS_IN_BLOCK_ART = 0
POS_IN_BLOCK_REL = 1


class BlockFinder(object):

    def __init__(self, company_id, matches_name):
        self._matchloader = MatchLoader(company_id, matches_name)
        self._tokens = TokenLoader(company_id)
        self._br = ConfigReader().get('MARKER_BR')

    def print_all_matching_blocks(self, min_len, max_len):
        for release_id in self._matchloader.get_release_ids():
            for article_id in self._matchloader.get_article_ids(release_id):
                blocks = self._matchloader.get_matches(release_id, article_id)
                for block in blocks:
                    i = block[0] 
                    j = block[1] 
                    k = block[2] 

                    rel_match = self._tokens.get_stripped_release_token_block(release_id, j,j+k)

                    if len(rel_match) >= min_len and len(rel_match) < max_len:
                        mb = ' '.join(rel_match)
                        mb = mb.replace(self._br, ' ')
                        print mb

    #prints blocks of min_length or larger occuring in more than one release -
    #   i.e., bad discriminators between releases
    def print_all_nondiscrim_release_blocks(self, min_len, max_len):
        blockset_dict = {}

        for release_id in self._matchloader.get_release_ids():

            blockset = set() #set of blocks for current release
            blockset_dict[release_id] = blockset
            
            for article_id in self._matchloader.get_article_ids(release_id):
                blocks = self._matchloader.get_matches(release_id, article_id)
                for block in blocks:
                    i = block[0] 
                    j = block[1] 
                    k = block[2] 

                    rel_match = self._tokens.get_stripped_release_token_block(release_id, j,j+k)
                    
                    if len(rel_match) >= min_len and len(rel_match) < max_len:
                        mb = ' '.join(rel_match)
                        mb = mb.replace(self._br, ' ')
                        mb = mb.lower().strip()
                        blockset.add(mb)

        #count occurances of each block per release
        bcounts = {}
        for release_id in blockset_dict:
            blockset = blockset_dict[release_id]
            for b in blockset:
                if b in bcounts:
                    bcounts[b] += 1
                else:
                    bcounts[b] = 1

        #print blocks which occur more than once per release
        result = [key for key in bcounts if bcounts[key] > 1]
        for r in result:
            print r
