import cPickle
import string
import nltk
from shared import common
from shared.config import ConfigReader


class SubjLexiconLoader(object):

    def __init__(self, strongonly=False):
        self._words = {}
        self._stems = {}
        self._stemmer = nltk.PorterStemmer()
        self._load_codes()
        self._load_lexicon(strongonly)

    def get_polarity(self, word, pos):
        if not pos in self._codes:
            pos_code = 'anypos'
        else:
            pos_code = self._codes[pos]

        key1 = word, pos_code
        key2 = word

        stemmed = self._stemmer.stem(word)
        key3 = stemmed, pos_code
        key4 = stemmed
        
        if key1 in self._words:
            return self._words[key1]
        elif key2 in self._words:
            return self._words[key2]
        elif key3 in self._stems:
            return self._stems[key3]
        elif key4 in self._stems:
            return self._stems[key4]
        else:
            return None

    def _load_lexicon(self, strongonly):        
        path = common.get_subjlexicon_path()
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                pairs = line.split()
                stype = pairs[0].split('=')[1]
                word = pairs[2].split('=')[1]
                pos_code = pairs[3].split('=')[1]
                stemmed = pairs[4].split('=')[1]
                polarity = pairs[5].split('=')[1]

                if strongonly and stype == 'weaksubj':
                    continue

                if pos_code == 'anypos':
                    key = word
                else:
                    key = word, pos_code

                if stemmed == 'n':
                    self._words[key] = polarity
                else:
                    self._stems[key] = polarity

    def _load_lexicon_stemmed(self):        
        path = common.get_subjlexicon_path(True)
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                line = line.split()
                key = line[0]
                if not key in self._dict:
                    self._dict[key] = line[2]
                key = line[0], line[1]
                if not key in self._dict:
                    self._dict[key] = line[2]

    def _load_codes(self):
        self._codes = {}
        self._codes['JJ']   = 'adj' 
        self._codes['JJR']  = 'adj'
        self._codes['JJS']  = 'adj'
        self._codes['NN']   = 'noun'
        self._codes['NNS']  = 'noun'
        self._codes['NNP']  = 'noun'
        self._codes['NNPS'] = 'noun'
        self._codes['RB']   = 'adverb'
        self._codes['RBR']  = 'adverb'
        self._codes['RBS']  = 'adverb'
        self._codes['WRB']  = 'adverb'
        self._codes['VB']   = 'verb' 
        self._codes['VBD']  = 'verb'
        self._codes['VBG']  = 'verb'
        self._codes['VBN']  = 'verb'
        self._codes['VBP']  = 'verb'
        self._codes['VBZ']  = 'verb'
