import cPickle
import os.path
import string
from shared import common
from shared.config import ConfigReader


class ScoreLoader(object):

    def __init__(self, company_id):
        self._load_dictionaries(company_id)

    def count_pos_rel_sentences(self, release_id):
        return self._rel_dict[release_id].number_of_pos_sents()

    def count_neg_rel_sentences(self, release_id):
        return self._rel_dict[release_id].number_of_neg_sents()

    def count_posneg_rel_sentences(self, release_id):
        return self._rel_dict[release_id].number_of_posneg_sents()

    def count_subj_rel_sentences(self, release_id):
        return self._rel_dict[release_id].number_of_subj_sents()

    def count_all_rel_sentences(self, release_id):
        return self._rel_dict[release_id].number_of_all_sents()

    def count_pos_rel_words(self, release_id):
        return self._rel_dict[release_id].number_of_pos_words()

    def count_neg_rel_words(self, release_id):
        return self._rel_dict[release_id].number_of_neg_words()

    def count_pos_art_sentences(self, article_id):
        return self._art_dict[article_id].number_of_pos_sents()

    def count_neg_art_sentences(self, article_id):
        return self._art_dict[article_id].number_of_neg_sents()

    def count_posneg_art_sentences(self, article_id):
        return self._art_dict[article_id].number_of_posneg_sents()

    def count_subj_art_sentences(self, article_id):
        return self._art_dict[article_id].number_of_subj_sents()

    def count_all_art_sentences(self, article_id):
        return self._art_dict[article_id].number_of_all_sents()

    def count_pos_art_words(self, article_id):
        return self._art_dict[article_id].number_of_pos_words()

    def count_neg_art_words(self, article_id):
        return self._art_dict[article_id].number_of_neg_words()

    def _load_dictionaries(self, company_id):
        self._rel_dict = {}
        path_rel = common.get_sentiment_scores_path(company_id) + '-' + common.DOCTYPE_PR
        self._load_dict(path_rel, self._rel_dict)
        
        self._art_dict = {}
        path_art = common.get_sentiment_scores_path(company_id) + '-' + common.DOCTYPE_NEWS
        self._load_dict(path_art, self._art_dict)

    def _load_dict(self, path, dic):
        with open(path) as f:
            lines = f.readlines()

            is_first_line = True
            current_id = -1
            pos_sents = 0
            neg_sents = 0
            posneg_sents = 0
            subj_sents = 0
            all_sents = 0
            pos_words = 0
            neg_words = 0

            for line in lines:
                pairs = line.split()
                doc_id = int(pairs[0].split('=')[1])
                # sent_id = int(pairs[1].split('=')[1])
                pos = int(pairs[2].split('=')[1])
                neg = int(pairs[3].split('=')[1])

                if doc_id == current_id or is_first_line:
                    is_first_line = False
                    current_id = doc_id

                    all_sents += 1

                    if pos > 0 and neg == 0:
                        pos_sents += 1
                        subj_sents += 1
                    elif pos == 0 and neg > 0: 
                        neg_sents += 1
                        subj_sents += 1
                    elif pos > 0 and neg > 0: 
                        posneg_sents += 1
                        subj_sents += 1

                    pos_words += pos
                    neg_words += neg

                else:
                    newdoc = Document(current_id, pos_sents, neg_sents, posneg_sents, \
                            subj_sents, all_sents, pos_words, neg_words)
                    dic[current_id] = newdoc

                    #resert everything
                    current_id = doc_id
                    pos_sents = 0
                    neg_sents = 0
                    posneg_sents = 0
                    subj_sents = 0
                    all_sents = 0
                    pos_words = 0
                    neg_words = 0

                #write last record
                newdoc = Document(current_id, pos_sents, neg_sents, posneg_sents, \
                        subj_sents, all_sents, pos_words, neg_words)

                dic[current_id] = newdoc


class Document(object):

    def __init__(self, doc_id, pos_sents, neg_sents, posneg_sents, subj_sents,\
            all_sents, pos_words, neg_words):
        self._data = int(doc_id), int(pos_sents), int(neg_sents), \
                int(posneg_sents), int(subj_sents), int(all_sents), \
                int(pos_words), int(neg_words)

    def id(self):
        return self._data[0]

    def number_of_pos_sents(self):
        return self._data[1]

    def number_of_neg_sents(self):
        return self._data[2]

    def number_of_posneg_sents(self):
        return self._data[3]

    def number_of_subj_sents(self):
        return self._data[4]

    def number_of_all_sents(self):
        return self._data[5]

    def number_of_pos_words(self):
        return self._data[6]

    def number_of_neg_words(self):
        return self._data[7]
