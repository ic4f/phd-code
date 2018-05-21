import sys
import unicodedata
from HTMLParser import HTMLParser


class DataCleaner(object):

    def __init__(self, encoding='utf-8'):
        self._encoding = encoding
        self._load_dic()

    def clean(self, text):
        #make unicode
        u = text.decode(self._encoding)
        return self.clean_unicode(u)
    
    #used for releases: the output from soup is unicode
    def clean_unicode(self, u):
        hp = HTMLParser()

        #translate important characters
        u = u.translate(self._dic)
       
        #unescape HTML entities and characters
        u = hp.unescape(u)
        
        #make ascii: transform or ignore the rest of non-ascii chars
        a = unicodedata.normalize('NFKD', u).encode('ascii', 'ignore')

        #clean upremaining entities
        a = hp.unescape(a)

        a = a.replace('`', "'") #replace apostrophies with single quotes
        a = a.replace("''", '"') #replace double single quotes with regular doubloe quotes
        return a

    def _load_dic(self):
        self._dic = {}
        self._dic[ord(u'\u2018')] = ord("'")  #Single curved quote, left
        self._dic[ord(u'\u2019')] = ord("'")  #Single curved quote, right
        self._dic[ord(u'\u2019')] = ord("'")  #Single curved quote, right
        self._dic[ord(u'\u201B')] = ord("'")  #single reversed comma, quotation mark
        self._dic[ord(u'\u201F')] = ord("'")  #double reversed comma, quotation mark
        self._dic[ord(u'\u301D')] = ord("'")  #reversed double prime quotation mark
        self._dic[ord(u'\u301E')] = ord("'")  #double prime quotation mark
        self._dic[ord(u'\uFF02')] = ord("'")  #Halfwidth and Fullwidth Forms
        self._dic[ord(u'\u0060')] = ord("'")  #GRAVE ACCENT
        self._dic[ord(u'\u00B4')] = ord("'")  #ACUTE ACCENT

        self._dic[ord(u'\u201C')] = ord('"')  #Double curved quote, or "curly quote," left                                    
        self._dic[ord(u'\u201D')] = ord('"')  #Double curved quote, right
        self._dic[ord(u'\uFF07')] = ord('"')  #Halfwidth and Fullwidth Forms
        self._dic[ord(u'\xab')] = ord('"')    #Halfwidth and Fullwidth Forms
        self._dic[ord(u'\xbb')] = ord('"')    #Halfwidth and Fullwidth Forms

        self._dic[ord(u'\u00AE')] = None  #registered trademark
        self._dic[ord(u'\u2122')] = None  #trademark sign

        self._dic[ord(u'\u2010')] = ord('-')  #dash
        self._dic[ord(u'\u2011')] = ord('-')  #dash
        self._dic[ord(u'\u2012')] = ord('-')  #dash
        self._dic[ord(u'\u2013')] = ord('-')  #dash
        self._dic[ord(u'\u2014')] = ord('-')  #dash
        self._dic[ord(u'\u2015')] = ord('-')  #dash
        self._dic[ord(u'\u2500')] = ord('-')  #dash
        self._dic[ord(u'\u2212')] = ord('-')  #dash
