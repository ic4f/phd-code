import sys
import os.path
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from data.tokens import TokenLoader
from shared.config import ConfigReader 
from shared.tokenizer import Tokenizer
from shared import common
from data.subjlexicon import SubjLexiconLoader

PR_CODE = 'R'
NEWS_CODE = 'A'


class SentenceWriter(object):
    
    def __init__(self, company_id, release_ids, article_ids, output_name):
        self._company_id = company_id
        self._release_ids = release_ids
        self._article_ids = article_ids
        self._output_name = output_name

        self._releases = ReleaseLoader(company_id).get_releases()
        self._articles = ArticleLoader(company_id).get_articles()

        self._tokenizer = Tokenizer()
        self._lexicon = SubjLexiconLoader()

        self._make_dirs()


    def write_and_calculate(self):
        words_rel_pos = []
        words_art_pos = []
        words_rel_neg = []
        words_art_neg = []
        scores_rel = []
        scores_art = []

        for i, release_id in enumerate(self._release_ids):
            print 'Processing release {0} of {1}'.format(i+1, len(self._release_ids))
            release = self._releases[release_id]
            text = release.title() + '.\n' + release.body()
            self._write_text(release_id, text, PR_CODE, common.DOCTYPE_PR, words_rel_pos, words_rel_neg, scores_rel)


        for i, article_id in enumerate(self._article_ids):
            print 'Processing article {0} of {1}'.format(i+1, len(self._article_ids))
            article = self._articles[article_id]
            text = article.headline() + '.\n' + article.body()
            self._write_text(article_id, text, NEWS_CODE, common.DOCTYPE_NEWS, words_art_pos, words_art_neg, scores_art)

        #save word lists and scores
        path = common.get_sentiment_scores_path(self._company_id) + '-' + common.DOCTYPE_PR
        with open(path, 'w') as f:
            f.write('\n'.join(scores_rel))

        path = common.get_sentiment_scores_path(self._company_id) + '-' + common.DOCTYPE_NEWS
        with open(path, 'w') as f:
            f.write('\n'.join(scores_art))
        
        path = common.get_sentiment_words_pos_path(self._company_id) + '-' + common.DOCTYPE_PR
        with open(path, 'w') as f:
            f.write('\n'.join(words_rel_pos))

        path = common.get_sentiment_words_neg_path(self._company_id) + '-' + common.DOCTYPE_PR
        with open(path, 'w') as f:
            f.write('\n'.join(words_rel_neg))

        path = common.get_sentiment_words_pos_path(self._company_id) + '-' + common.DOCTYPE_NEWS
        with open(path, 'w') as f:
            f.write('\n'.join(words_art_pos))

        path = common.get_sentiment_words_neg_path(self._company_id) + '-' + common.DOCTYPE_NEWS
        with open(path, 'w') as f:
            f.write('\n'.join(words_art_neg))


    def _write_text(self, text_id, text, code, doctype, words_pos, words_neg, scores):
        html = []
        name = common.get_company_name(self._company_id)

        html.append('<h4>{0}</h4>'.format(name))
        html.append('\n<table class="tbl-main" cellpadding="5" border="1">')
        html.append('<tr><td>ID</td><td>text</td><td>POS</td><td>NEG</td><td>BOTH</td><td>N/A</td></tr>')

        sents = self._tokenizer.get_sentences(text)
        for i, s in enumerate(sents):

            pos = 0
            neg = 0

            tokens = word_tokenize(s)
            tagged = pos_tag(tokens)
            sb = []
            for pair in tagged:
                word = pair[0]
                polarity = self._lexicon.get_polarity(word, pair[1])

                if polarity == 'positive':
                    sb.append('<span class="pol-positive">{0}</span>'.format(word))
                    words_pos.append(word)
                    pos += 1
                elif polarity == 'negative':
                    sb.append('<span class="pol-negative">{0}</span>'.format(word))
                    words_neg.append(word)
                    neg += 1
                else:
                    sb.append(pair[0])

            scores.append('doc-id={0} sent-id={1} pos={2} neg={3}'.format(text_id, i+1, pos, neg))

            sent_id = '{0}-{1}-{2}-{3}'.format(self._company_id, code, text_id, i+1)
            html.append('<tr valign="top">')
            html.append('<td>{0}</td>'.format(sent_id))
            html.append('<td>{0}</td>'.format(' '.join(sb)))
            html.append('<td> </td><td> </td><td> </td><td> </td></tr>')
        
        html.append('\n</table>')

        path = self._get_filepath(doctype, text_id)
        self._write_html_to_file(path, '\n'.join(html))


    def _get_filepath(self, doctype, text_id):
        path_dir = common.get_sents_path(self._output_name, self._company_id)
        path_subdir = os.path.join(path_dir, doctype)
        return os.path.join(path_subdir, str(text_id))

    def _make_dirs(self):
        path = common.get_sents_path(self._output_name, self._company_id)
        if not os.path.exists(path):
            os.mkdir(path)

        rel_path = os.path.join(path, common.DOCTYPE_PR)
        if not os.path.exists(rel_path):
            os.mkdir(rel_path)
        
        art_path = os.path.join(path, common.DOCTYPE_NEWS)
        if not os.path.exists(art_path):
            os.mkdir(art_path)

    def _write_html_to_file(self, output_path, html):
        with open(output_path, 'w') as f:
            f.write('<html>\n<head>')
            f.write('\n\t<link rel="stylesheet" type="text/css" href="../../../styles.css">')
            f.write('\n</head>\n<body>\n')
            f.write(html)
            f.write('\n\n</body>\n</html>')
