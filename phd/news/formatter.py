import datetime
import os
import sys
import re
from shared import common
from shared.config import ConfigReader
from shared.data_cleaner import DataCleaner


class Formatter(object):

    def __init__(self, company_id, output_path):
        self._company_id = company_id
        self._output_path = output_path
        
        self._sb_list = []
        self._sb_text = []
        self._counter = 0

        self._init_regex()
        self._set_flags(False, False, False, False)
        self._reset_content()
        self._load_nonpubs()

    def run(self):
        path = self._get_input_path()
        with open(path) as f:
            self._scan(f)
        self._write_files()

    def _write_files(self):
        list_file = common.get_list_file_name(self._company_id)
        path_list = os.path.join(self._output_path, list_file)
        path_text = os.path.join(self._output_path, self._company_id)

        dc = DataCleaner('utf-8')
        clean_list = dc.clean(''.join(self._sb_list))
        clean_text = dc.clean(''.join(self._sb_text))
        
        with open(path_list, 'w') as f:
            f.write(clean_list)
        with open(path_text, 'w') as f:
            f.write(clean_text)


    def _scan(self, f):        
        write = False #no doc has been read yet: there's nothing to write
        while True:
            line = f.readline()
            if line == '':
                self._write_doc() #flush the last doc
                break
            
            if self._re_start.search(line): #found new doc 
                if write: #if there is a previous doc to write 
                    self._write_doc()
                self._set_flags(True, False, False, False)
                
            elif line.startswith('HEADLINE'):
                self._set_flags(False, True, False, False)
                write = True
                line = line[10:] #drop 'HEADLINE: '

            elif line.startswith('BYLINE'):
                self._set_flags(False, False, True, False)
                write = True
                line = line[8:] #drop 'BYLINE: '
                if line.lower().startswith('by '):
                    line = line[3:] #drop 'By |by '
                
            if line.strip() == 'BODY:': #use this to protect against 'BODY:' in the text
                self._set_flags(False, False, False, True)
                write = True
                line = line[6:] #drop 'BODY: '

            if self._ishead:
                line = line.strip()
                if len(line) > 0:
                    self._head.append(line)

            if self._isheadline:
                line = line.strip() 
                self._headline = self._headline + ' ' + line

            if self._isbyline:
                line = line.strip()
                self._byline = self._byline + ' ' + line
            
            if self._isbody:
                if not (line.startswith('DOCUMENT-TYPE: ') or
                    line.startswith('PUB-TYPE: ') or
                    line.startswith('ORGANIZATION: ') or
                    line.startswith('LOAD-DATE: ')):
                    self._body.append(line)


    def _write_doc(self):
        self._parse_head()

        pub = self._pub.strip()
        byline = self._byline.strip()
        headline = self._headline.strip()
        body = self._format_body(self._body)

        if len(byline) > 100:
            byline = byline[:100]
        
        if len(headline) > 500:
            headline = headline[:500]

        if self._date is None:
            raise Exception('Found no date for <<{0}>> in <<{1}>>'.format(headline, pub))
        else:
            date = self._date.strftime('%Y-%m-%d')

        self._counter += 1

        self._sb_list.append('LOTW-ID: {0}\n'.format(self._counter))
        self._sb_list.append('LOTW-PUB: {0}\n'.format(pub))
        self._sb_list.append('LOTW-DATE: {0}\n'.format(date))
        self._sb_list.append('LOTW-HEADLINE: {0}\n'.format(headline))
        self._sb_list.append('LOTW-BYLINE: {0}\n\n'.format(byline))

        self._sb_text.append('LOTW-ID: {0}\n'.format(self._counter))
        self._sb_text.append('{0}\n\n\n\n'.format(body))

        self._set_flags(False, False, False, False)
        self._reset_content()

    def _format_body(self, body):
        newbody = []
        for line in body:
            line = line.replace('\r\n', '\n') #kill windows/dos carriage returns
            line = line.rstrip() #kill line breaks at the end of line
            if len(line) > 0: #if there is text, add whitspace
                line = line + ' '
            else:
                line = '\n\n' #otherwise, add a line break
            newbody.append(line)
       
        text = ''.join(newbody).strip()
        pattern = re.compile(r'\n{3,}')
        return pattern.sub('\n\n', text)

    def _parse_head(self):
        publines = []
        header = self._head
        for line in header:
            linelower = line.lower()
            if '2012' in line and not 'copyright' in linelower:
                self._parse_date(line)
            else:
                ispub = True
                for nonpub in self._nonpubs: #check line against non-pub stopwords
                    if nonpub in linelower:
                        ispub = False
                if ispub:
                    publines.append(line)

        #special handling for this dataset only!
        if len(publines) == 2 and not (publines[0] == 'The New York Times' \
            and publines[1] == 'The International Herald Tribune'):
            publines[0] = publines[0] + ' ----- ' + publines[1]

        if publines[0].strip() == 'Richmond Times Dispatch (Virginia)':
            publines[0] = 'Richmond Times-Dispatch (Virginia)'
        elif publines[0].strip() == 'The New York Times ----- National':
            publines[0] = 'The New York Times'

        self._pub = publines[0]

    def _parse_date(self, text):
        text = text.replace(',', ' ')
        words = text.split()
        if len(words) == 2:        
            self._date = datetime.datetime.strptime(text, '%B %Y')
        elif len(words) == 3:        
            self._date = datetime.datetime.strptime(text, '%B %d %Y')
        elif len(words) == 4:
            self._date = datetime.datetime.strptime(text, '%B %d %Y %A')
        elif len(words) == 7:
            words = words[:3]
            text = ' '.join(words)
            self._date = datetime.datetime.strptime(text, '%B %d %Y')
        else:
            print len(words)
            raise Exception('ERROR: cannot parse date: {0}'.format(text))

    def _init_regex(self):
        months = '(January)|(February)|(March)|(April)|(May)|(June)| \
            (July)|(August)|(September)|(October)|(November)|(December)'
        days = '(Monday)|(Tuesday)|(Wednesday)|(Thursday)|(Friday)|(Saturday)|(Sunday)'
        pattern_date = r'^\s*' + months + '\s\d+,\s\d+\s' + days + '\s*$'
        pattern_start = r'^\s*\d+\s+of\s+\d+\s+DOCUMENTS\s*$'
        
        self._re_start = re.compile(pattern_start)
        self._re_date = re.compile(pattern_date)

    def _set_flags(self, ishead, isheadline, isbyline, isbody):
        self._ishead = ishead
        self._isheadline = isheadline
        self._isbyline = isbyline
        self._isbody = isbody

    def _reset_content(self):
        self._head = []
        self._pub = ''
        self._date = None
        self._headline = ''
        self._byline = ''
        self._body = []

    def _load_nonpubs(self):
        self._nonpubs = set()
        cfr = ConfigReader()
        path = os.path.abspath(cfr.get('NONPUBS'))
        with open(path) as f:
            for line in f.readlines():
                line = line.strip().lower()
                if len(line) > 0:
                    self._nonpubs.add(line)

    def _get_input_path(self):
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('DOWNLOADED_NEWS')
        path2 = os.path.join(root, path1)
        return os.path.join(path2, self._company_id)
