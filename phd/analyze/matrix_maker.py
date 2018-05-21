from __future__ import division
import sys
from data.matches import MatchLoader 
from data.matches import MatchMaker
from data.tokens import TokenLoader
from data.scores import ScoreLoader


class MatrixMaker(object):

    def __init__(self, match_name):
        self._match_name = match_name

    def print_pairs(self):
        sb = []
        for company_id in range(1, 41): 
            matches = MatchLoader(company_id, self._match_name)
            for release_id in matches.get_release_ids():

    def print_matrix(self):
        sb = []
        sb.append('co-id, rel-id, art-id, rel-len, art-len, rel-used, art-added, rel-subj-score, art-subj-score, rel-sent-score, art-sent-score\n')
#        sb.append('co-id rel-id art-id rel-len art-len rel-used art-added rel-subj-score art-subj-score rel-sent-score art-sent-score\n')

        for company_id in range(1, 41):
            matches = MatchLoader(company_id, self._match_name)
            tokens = TokenLoader(company_id)
            scores = ScoreLoader(company_id)

            for release_id in matches.get_release_ids():
                rel_tokens = tokens.get_stripped_release_token_block(release_id, 0, sys.maxint)

                #release subjectivity score
                rel_subj = scores.count_subj_rel_sentences(release_id) / scores.count_all_rel_sentences(release_id)
                #release sentiment score
                if scores.count_subj_rel_sentences(release_id) == 0:
                    rel_sents = 0
                else:
                    pos_minus_neg = scores.count_pos_rel_sentences(release_id) - scores.count_neg_rel_sentences(release_id)
                    rel_sent = pos_minus_neg / scores.count_subj_rel_sentences(release_id)

                for article_id in matches.get_article_ids(release_id):
                    art_tokens = tokens.get_stripped_article_token_block(article_id, 0, sys.maxint)

                    blocks = matches.get_matches(release_id, article_id)
                    blocklen = 0
                    for b in blocks:
                        start = b[1]
                        length = b[2]
                        end = start + length
                        block_tokens = tokens.get_stripped_release_token_block(release_id, start, end)
                        blocklen += len(block_tokens)

                    rel_used = blocklen/len(rel_tokens)

                    art_added = 1 - blocklen/len(art_tokens)

                    #article subjectivity score
                    art_subj = scores.count_subj_art_sentences(article_id) / scores.count_all_art_sentences(article_id)
                    #article sentiment score
                    if scores.count_subj_art_sentences(article_id) == 0:
                        art_sents = 0
                    else:
                        pos_minus_neg = scores.count_pos_art_sentences(article_id) - scores.count_neg_art_sentences(article_id)
                        art_sent = pos_minus_neg / scores.count_subj_art_sentences(article_id)

                    sb.append('{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}\n'.format( \
#                    sb.append('{0} {1} {2} {3} {4} {5} {6} {7} {8} {9} {10}\n'.format( \
                        company_id, release_id, article_id, len(rel_tokens), len(art_tokens), rel_used, art_added, rel_subj, art_subj, rel_sent, art_sent))

        text = ''.join(sb)
        print text
