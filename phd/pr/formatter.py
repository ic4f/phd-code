import os
import os.path
import sys
import re
from bs4 import BeautifulSoup
from shared import common
from shared.config import ConfigReader
from shared.data_cleaner import DataCleaner
import source_factory


class Formatter(object):

    def __init__(self, company_id, output_path):
        self._company_id = company_id
        self._output_path = output_path
        self._src = source_factory.get_class(self._company_id)       
        self._marker = 'LOTW-BR-MARKER'
        self._pattern1 = re.compile('\n\s*')
        self._pattern2 = re.compile('(LOTW-BR-MARKER\s*)+')
        self._pattern3 = re.compile(' [ ]+')
        self._dc = DataCleaner(self._src.get_encoding())

        self._load_replacements()                
        self._load_linebreaks()                
        self._load_path()
        self._load_list()

    def run(self):
        sb_list = []
        sb_text = []
        counter = 0
        for item in self._list:
            #we don't care about item[0] - it's the id assigned during crawl -
            #   which we will override here even if it's identical
            date        = item[1]
            title       = item[2]
            url         = item[3]
            counter += 1

            path = os.path.join(self._path_dir, str(counter))
            with open(path) as f:
                html = f.readlines()
            body = self._format_body(''.join(html), title)

            #special handling for delta's dates
            if self._company_id == '24':
                date = self._src.get_date_from_body(body)

            sb_list.append('LOTW-ID: {0}\n'.format(counter))
            sb_list.append('LOTW-DATE: {0}\n'.format(date))
            sb_list.append('LOTW-TITLE: {0}\n'.format(title))
            sb_list.append('LOTW-URL: {0}\n\n'.format(url))
            sb_text.append('LOTW-ID: {0}\n'.format(counter))
            sb_text.append('{0}\n\n\n\n'.format(body))

        self._write_files(sb_list, sb_text)

    def _write_files(self, sb_list, sb_text):
        list_file = common.get_list_file_name(self._company_id)
        path_list = os.path.join(self._output_path, list_file) #refactor
        path_text = os.path.join(self._output_path, self._company_id)

        clean_list = self._dc.clean(''.join(sb_list))
        clean_text = ''.join(sb_text) #this has been cleaned in _format_body()
        
        with open(path_list, 'w') as f:
            f.write(clean_list)

        with open(path_text, 'w') as f:
            f.write(clean_text)

    def _format_body(self, html, title):
        html = html.replace('\r\n', '\n') #kill windows/dos carriage returns
        for s in self._br:
            html = html.replace(s, self._marker + s) #mark all future line breaks
            html = html.replace(s.upper(), self._marker + s) #check for caps in tags
        
        body = self._src.get_text(html) #kill tags
        body = self._dc.clean_unicode(body) #clean data
        body = self._pattern1.sub(' ', body) #kill line breaks (MUST add a space instead!)
        body = self._pattern2.sub('\n\n', body) #insert my line breaks 
        body = self._pattern3.sub(' ', body) #kill extra spaces
        
        for s in self._replacements:
            body = body.replace(s, self._replacements[s])

        body = body.strip()
        if body.startswith(title): #get rid of title
            body = body[len(title):]
        return body.strip()

    def _load_replacements(self):
        self._replacements = {}
        self._replacements['&#8216;'] = "'"
        self._replacements['&#8217;'] = "'"
        self._replacements['&lsquo;'] = "'"
        self._replacements['&rsquo;'] = "'"
        self._replacements['&#8220;'] = '"'
        self._replacements['&#8221;'] = '"'
        self._replacements['&ldquo;'] = '"'
        self._replacements['&rdquo;'] = '"'
        self._replacements['&#8249;'] = "'"
        self._replacements['&#8250;'] = "'"
        self._replacements['&lsaquo;'] = "'"
        self._replacements['&rsaquo;'] = "'"

    def _load_linebreaks(self):                
        self._br = set()
        self._br.add('<p>')
        self._br.add('<p ')
        self._br.add('<li>')
        self._br.add('<li ')
        self._br.add('<div')
        self._br.add('<h1')
        self._br.add('<h2')
        self._br.add('<h3')
        self._br.add('<h4')
        self._br.add('<h5')
        self._br.add('<h6')
        self._br.add('<table')
        self._br.add('<tr')
        self._br.add('<td')
        self._br.add('<br>')
        self._br.add('<br ')
        self._br.add('<blockquote')
        self._br.add('<caption')
        self._br.add('<dd')
        self._br.add('<dl')
        self._br.add('<dt')
        self._br.add('<form')
        self._br.add('<iframe')
        self._br.add('<input')
        self._br.add('<label')
        self._br.add('<pre')

    def _load_path(self):
        cfr = ConfigReader()
        root = cfr.get('ROOT_ORIGINAL')
        path1 = cfr.get('DOWNLOADED_PR')
        path2 = os.path.join(root, path1)
        self._path_dir = os.path.join(path2, self._company_id)

    def _load_list(self):
        self._list = []

        filename = common.get_list_file_name()
        path = os.path.join(self._path_dir, filename)

        with open(path) as f:
            write = False #no doc has been read yet: there's nothing to write
            while True:
                line = f.readline()
                if line == '':
                    self._add_to_list(release_id, date, title, url) #flush the last doc
                    break
                if line.startswith('LOTW-ID: '): #found new doc
                    if write: #write if there is a previous doc to write 
                        self._add_to_list(release_id, date, title, url)
                    release_id = line[9:].strip()
                    write = True
                elif line.startswith('LOTW-DATE: '):
                    date = line[11:].strip()
                elif line.startswith('LOTW-TITLE: '):
                    title = line[12:].strip() 
                elif line.startswith('LOTW-URL: '):
                    url = line[10:].strip() 

    def _add_to_list(self, release_id, date, title, url):
        item = [release_id, date, title, url]
        self._list.append(item)
