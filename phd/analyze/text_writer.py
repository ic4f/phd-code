import sys
import os.path
from data.tokens import TokenLoader
from shared.config import ConfigReader 
from shared import common


class TextWriter(object):
    
    def __init__(self, company_id, release_ids, article_ids, output_name):
        self._company_id = company_id
        self._release_ids = release_ids
        self._article_ids = article_ids
        self._output_name = output_name
        self._tokens = TokenLoader(company_id)        
        self._make_dirs()

    def write(self):    
        br = ConfigReader().get('MARKER_BR')
        for release_id in self._release_ids:

            tokens = self._tokens.get_release_tokens(release_id, False)
            text = ' '.join(tokens)
            text = text.replace(br, '\n')
            path = self._get_filepath(common.DOCTYPE_PR, release_id)
            with open(path, 'w') as f:
                f.write(text)
            
        for article_id in self._article_ids:
            tokens = self._tokens.get_article_tokens(article_id, False)
            text = ' '.join(tokens)
            text = text.replace(br, '\n')
            path = self._get_filepath(common.DOCTYPE_NEWS, article_id)
            with open(path, 'w') as f:
                f.write(text)

    def _get_filepath(self, doctype, text_id):
        path_dir = common.get_text_path(self._output_name, self._company_id)
        path_subdir = os.path.join(path_dir, doctype)
        return os.path.join(path_subdir, str(text_id))

    def _make_dirs(self):
        path = common.get_text_path(self._output_name, self._company_id)
        if not os.path.exists(path):
            os.mkdir(path)

        rel_path = os.path.join(path, common.DOCTYPE_PR)
        if not os.path.exists(rel_path):
            os.mkdir(rel_path)
        
        art_path = os.path.join(path, common.DOCTYPE_NEWS)
        if not os.path.exists(art_path):
            os.mkdir(art_path)
