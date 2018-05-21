import os
import string
from shared import common


# this class not used in final version
class BlockMaker(object):

    def __init__(self, company_id, blocks_name):
       self._company_id = company_id
       self._blocks_name = blocks_name
       self._blocks = []

    def add_block(self, block):
        self._blocks.append(block)
    
    def save(self):
        dir_path = common.get_blocks_path(self._blocks_name)
        path = os.path.join(dir_path, str(self._company_id))
        with open(path, 'w') as f:
            for b in self._blocks:
                f.write('{0}\n'.format(b.strip()))


class BlockLoader(object):

    def __init__(self, company_id, blocks_name):
        self._load(company_id, blocks_name)

    def get_blocks(self):
        return self._blocks
    
    def _load(self, company_id, blocks_name):        
        dir_path = common.get_blocks_path(blocks_name)
        path = os.path.join(dir_path, str(company_id))
        with open(path) as f:
            self._blocks = [line.strip() for line in f.readlines()]
