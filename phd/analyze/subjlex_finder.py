from __future__ import division
import sys
import nltk
from data.tokens import TokenLoader
from data.matches import MatchLoader
from shared.config import ConfigReader 
from shared import common
from data.subjlexicon import SubjLexiconLoader
from data.postags import POSTagLoader


class SubjlexFinder(object):

    def __init__(self, company_id):
        self._company_id = company_id

    def run(self):
        ploader = POSTagLoader(self._company_id, 'final')

        rel_tags = ploader.get_release_tags(68)
        art_tags = ploader.get_article_tags(65)

        lexicon = SubjLexiconLoader()

        pos = 0
        neg = 0
        neu = 0

        for pair in rel_tags:
            polarity = lexicon.get_polarity(pair[0], pair[1])
            if not polarity is None:
                if polarity == 'positive':
                    pos += 1
                    print pair[0] + ' ' + polarity
                if polarity == 'negative':
                    neg += 1
                    print pair[0] + ' ' + polarity
                if polarity == 'neutral':
                    neu += 1

        print pos
        print neg
        print neu

        pos = 0
        neg = 0
        neu = 0

        for pair in art_tags:
            polarity = lexicon.get_polarity(pair[0], pair[1])
            if not polarity is None:
                if polarity == 'positive':
                    pos += 1
                    print pair[0] + ' ' + polarity
                if polarity == 'negative':
                    neg += 1
                    print pair[0] + ' ' + polarity
                if polarity == 'neutral':
                    neu += 1

        print pos
        print neg
        print neu

        tloader = TokenLoader(self._company_id)

        id = int(sys.argv[1])
        tmp = tloader.get_release_tokens(1, False)
        tmp = tloader.get_article_tokens(id, False)

        tokens = ['\n' if t == br else t for t in tmp]

        pos = 0
        neg = 0
        neu = 0
        
        tagged = nltk.pos_tag(tokens)
        for t in tagged:
            polarity = lexicon.get_polarity(t[0], t[1])
            if not polarity is None:
                if polarity == 'positive':
                    pos += 1
                if polarity == 'negative':
                    neg += 1
                if polarity == 'neutral':
                    neu += 1
                
                print t[0] + ' ' + polarity

        print pos
        print neg
        print neu
        print t[1]
