import sys
from data.matches import MatchLoader 
from data.matches import MatchMaker
from data.tokens import TokenLoader


class MatchFilter(object):

    def __init__(self, company_id, match_name_in, match_name_out):
        self._company_id = company_id
        self._match_name_in = match_name_in
        self._match_name_out = match_name_out
        self._tokens = TokenLoader(company_id)

    def filter_exclude_pairs(self, pairs_name):
        matches = MatchLoader(self._company_id, self._match_name_in)
        maker = MatchMaker(self._company_id, self._match_name_out)
        pairs = PairLoader(self._company_id, pairs_name)

        for release_id in matches.get_release_ids():
            for article_id in matches.get_article_ids(release_id):
                if not pairs.has_pair(release_id, article_id):
                    blocks = matches.get_matches(release_id, article_id)
                    maker.add_blocks(release_id, article_id, blocks)
        maker.save()

    def filter_by_min_len(self, min_len):
        matches = MatchLoader(self._company_id, self._match_name_in)
        maker = MatchMaker(self._company_id, self._match_name_out)

        for release_id in matches.get_release_ids():
            for article_id in matches.get_article_ids(release_id):
                
                blocks = matches.get_matches(release_id, article_id)
                newblocks = []
                for b in blocks:
                    start = b[1] #release start
                    length = b[2]
                    end = start + length
                    tkns = self._tokens.get_stripped_release_token_block(release_id, start, end)
                    if len(tkns) >= min_len:
                        newblocks.append(b)
                    if len(newblocks) > 0:
                        maker.add_blocks(release_id, article_id, newblocks)
        maker.save()
