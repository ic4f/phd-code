import sys
import os.path
import cPickle
from shared import common


class SubsetMaker(object):

    def __init__(self):
        self._pr_dict = {}
        self._news_dict = {}

    def save(self, subset_name):
        path = common.get_pickled_subset_path(subset_name, common.DOCTYPE_PR)
        with open(path, 'wb') as f:
            cPickle.dump(self._pr_dict, f, -1)

        path = common.get_pickled_subset_path(subset_name, common.DOCTYPE_NEWS)
        with open(path, 'wb') as f:
            cPickle.dump(self._news_dict, f, -1)

    def add_release(self, company_id, release_id):
        if not company_id in self._pr_dict:
            pr_set = set()
            self._pr_dict[company_id] = pr_set
        else:
            pr_set = self._pr_dict[company_id]
        pr_set.add(release_id)

    def add_article(self, company_id, article_id):
        if not company_id in self._news_dict:
            news_set = set()
            self._news_dict[company_id] = news_set
        else:
            news_set = self._news_dict[company_id]
        news_set.add(article_id)


class SubsetLoader(object):

    def __init__(self, subset_name):
        self._pr_dict = self._unpickle_subset(subset_name, common.DOCTYPE_PR)
        self._news_dict = self._unpickle_subset(subset_name, common.DOCTYPE_NEWS)

    def get_pr_dictionary(self):
        return self._pr_dict

    def get_news_dictionary(self):
        return self._news_dict

    def get_pr_idset(self, company_id):
        return self._pr_dict[company_id]

    def get_news_idset(self, company_id):
        return self._news_dict[company_id]

    def print_size(self):
        print "COUNTING PR:"
        for key in sorted(self._pr_dict):
            print '{0}: {1}'.format(key, len(self._pr_dict[key]))

        print "COUNTING NEWS:"
        for key in sorted(self._news_dict):
            print '{0}: {1}'.format(key, len(self._news_dict[key]))

    def print_contents(self):
        print "PRINTING PR:"
        for key in sorted(self._pr_dict):
            print '{0}: {1}\n'.format(key, self._pr_dict[key])

        print "PRINTING NEWS:"
        for key in sorted(self._news_dict):
            print '{0}: {1}\n'.format(key, self._news_dict[key])

    def _unpickle_subset(self, subset_name, doctype):
        path = common.get_pickled_subset_path(subset_name, doctype)
        with open(path, 'rb') as f:
            return cPickle.load(f)
