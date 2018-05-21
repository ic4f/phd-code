import nltk
from nltk.tokenize import word_tokenize


class Tokenizer(object):
    
    def __init__(self):
        #create pre-trained sentence tokenizer: tokenizing words alone is incorrect
        self._s_tokenizer = nltk.data.load('/tokenizers/punkt/english.pickle') 

    def get_tokens(self, text):
        #tokenize text into sentences, arg must be False to prevent modification
        sents = self.get_sentences(text)
        #tokenize sentences into word-tokens
        t_sents = (word_tokenize(s) for s in sents)
        #return flattened token list
        return sum(t_sents, [])

    def get_sentences(self, text):
        return self._s_tokenizer.tokenize(text, realign_boundaries=False)
