import os.path
import string
from shared.config import ConfigReader 

DOCTYPE_PR = 'pr'
DOCTYPE_NEWS = 'news'


def get_sentiment_scores_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('SENTIMENT_SCORES')
    return os.path.join(dir_path, str(company_id))

def get_sentiment_words_pos_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('SENTIMENT_WORDS_POS')
    return os.path.join(dir_path, str(company_id))

def get_sentiment_words_neg_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('SENTIMENT_WORDS_NEG')
    return os.path.join(dir_path, str(company_id))

def get_list_file_name(company_id=None):
    name = 'list'
    if company_id == None:
        return name
    else:
        return '{0}-{1}'.format(company_id, name)

def get_subjlexicon_path(stemmed=False):
    cr = ConfigReader()
    if stemmed:
        return cr.get('SUBJLEXICON-STEMMED')
    else:
        return cr.get('SUBJLEXICON')

def get_postags_path():
    cr = ConfigReader()
    return cr.get('POSTAGS')

def get_rel_duplicates_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('DUPLICATES_REL')
    return os.path.join(dir_path, str(company_id))

def get_sents_path(sents_name, company_id):
    cr = ConfigReader()
    dir_path = cr.get('SENTS')
    subdir = os.path.join(dir_path, sents_name)
    return os.path.join(subdir, str(company_id))

def get_text_path(text_name, company_id):
    cr = ConfigReader()
    dir_path = cr.get('TEXT')
    subdir = os.path.join(dir_path, text_name)
    return os.path.join(subdir, str(company_id))

def get_art_duplicates_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('DUPLICATES_ART')
    return os.path.join(dir_path, str(company_id))

def get_blocks_path(blocks_name):
    cr = ConfigReader()
    dir_path = cr.get('BLOCKS')
    return os.path.join(dir_path, blocks_name)

def get_pairs_path(pairs_name):
    cr = ConfigReader()
    dir_path = cr.get('PAIRS')
    return os.path.join(dir_path, pairs_name)

def get_quotes_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('QUOTES')
    filename = '{0}'.format(company_id)
    return os.path.join(dir_path, filename)

def get_pickled_subset_path(subset_name, doctype):
    cr = ConfigReader()
    base = cr.get('PICKLED_SUBSETS')
    dir_path = os.path.join(base, subset_name)
    filename = '{0}.pickle'.format(doctype)
    return os.path.join(dir_path, filename)

def get_pickled_news_tokens_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('PICKLED_TOKENS_NEWS')
    filename = '{0}.pickle'.format(company_id)
    return os.path.join(dir_path, filename)

def get_pickled_pr_tokens_path(company_id):
    cr = ConfigReader()
    dir_path = cr.get('PICKLED_TOKENS_PR')
    filename = '{0}.pickle'.format(company_id)
    return os.path.join(dir_path, filename)

def get_pickled_matches_path(company_id, subset_name):
    cr = ConfigReader()
    dir_path = cr.get('PICKLED_MATCHES')
    path = os.path.join(dir_path, subset_name)
    filename = '{0}.pickle'.format(company_id)
    return os.path.join(path, filename)

def get_company_name(company_id):
    if company_id == 1:
        return 'Exxon Mobil'
    elif company_id == 2:
        return 'CVS Caremark'
    elif company_id == 3:
        return 'McKesson'
    elif company_id == 4:
        return 'J.P. Morgan Chase & Co.'
    elif company_id == 5:
        return 'Kroger'
    elif company_id == 6:
        return 'Archer Daniels Midland'
    elif company_id == 7:
        return 'MetLife'
    elif company_id == 8:
        return 'Home Depot'
    elif company_id == 9:
        return 'PepsiCo'
    elif company_id == 10:
        return 'State Farm Insurance Cos.'
    elif company_id == 11:
        return 'WellPoint'
    elif company_id == 12:
        return 'Fannie Mae'
    elif company_id == 13:
        return 'Boeing'
    elif company_id == 14:
        return 'Comcast'
    elif company_id == 15:
        return 'Merck'
    elif company_id == 16:
        return 'Lockheed Martin'
    elif company_id == 17:
        return 'Sunoco'
    elif company_id == 18:
        return 'Safeway'
    elif company_id == 19:
        return 'Johnson Controls'
    elif company_id == 20:
        return 'FedEx'
    elif company_id == 21:
        return 'Abbott Laboratories'
    elif company_id == 22:
        return 'United Continental Holdings'
    elif company_id == 23:
        return 'Liberty Mutual Insurance Group'
    elif company_id == 24:
        return 'Delta Air Lines'
    elif company_id == 25:
        return 'New York Life Insurance'
    elif company_id == 26:
        return 'Aetna'
    elif company_id == 27:
        return 'Sprint Nextel'
    elif company_id == 28:
        return 'Allstate'
    elif company_id == 29:
        return 'American Express'
    elif company_id == 30:
        return 'Deere'
    elif company_id == 31:
        return 'Amazon.com'
    elif company_id == 32:
        return 'Apple'
    elif company_id == 33:
        return 'Bank of America Corp.'
    elif company_id == 34:
        return 'Citigroup'
    elif company_id == 35:
        return 'Ford Motor'
    elif company_id == 36:
        return 'International Business Machines'
    elif company_id == 37:
        return 'Microsoft'
    elif company_id == 38:
        return 'Morgan Stanley'
    elif company_id == 39:
        return 'Target'
    elif company_id == 40:
        return 'Wells Fargo'
    else:
        raise Exception('Unknown company-id: {0}'.format(company_id))

def get_month_by_name(name):
    name = name.lower()
    if name == 'jan' or name == 'january':
        return 1
    elif name == 'feb' or name == 'february':
        return 2 
    elif name == 'mar' or name == 'march':
        return 3
    elif name == 'apr' or name == 'april':
        return 4
    elif name == 'may':
        return 5
    elif name == 'jun' or name == 'june':
        return 6
    elif name == 'jul' or name == 'july':
        return 7
    elif name == 'aug' or name == 'august':
        return 8
    elif name == 'sep' or name == 'september' or name == 'sept': #stupid intern coders!
        return 9
    elif name == 'oct' or name == 'october':
        return 10
    elif name == 'nov' or name == 'november':
        return 11
    elif name == 'dec' or name == 'december':
        return 12
    else:
        raise Exception('month not recognized: {0}'.format(name))
