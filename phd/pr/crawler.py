import sys
import os.path
import re
import datetime
from urllib import urlopen
from bs4 import BeautifulSoup
from shared.config import ConfigReader
import source_factory
from shared import common


#retrieves html of all pr (press release) pages for a source and stores them
#for further processing. Needs to be run once per company.
class Crawler(object):

    def __init__(self, company_id, output_path):
        self._company_id = company_id
        self._src = source_factory.get_class(self._company_id)
        self._count = 0
        self._sb = []
        self._load_path(output_path)

    def run(self, istest=False):
        self._istest = istest

        linkpages = self._src.get_linkpages() #get html of all 'links' pages
        count = 0
        for page in linkpages:
            count += 1
            print 'processing page {0} of {1}'.format(count, len(linkpages))
            self._get_html(page)

        self._write_list()
        print 'EXTRACTED {0} PAGES'.format(self._count)

    def _load_path(self, output_path):
        self._path_dir = os.path.join(output_path, self._company_id)
        if not os.path.exists(self._path_dir):
            os.mkdir(self._path_dir)

    def _write_list(self):
        path = os.path.join(self._path_dir, common.get_list_file_name())
        with open(path, 'w') as f:
            f.write(''.join(self._sb))


    def _get_html(self, page): #get html of each 'pr' page and store it
        soup = BeautifulSoup(page)
        links = soup(self._src.is_link)
        titles = soup(self._src.is_title)
        dates = soup(self._src.is_date)

        if self._istest: #this is for developign a new scraper
            print 'links: ' + str(len(links))
            print 'titles: ' + str(len(titles))
            print 'dates: ' + str(len(dates))

        if not(len(links) == len(titles) == len(dates)):
            raise Exception("number of links/titles/dates not equal")

        count = 0
        for i in range(len(links)):
            count += 1
            if count % 5 == 0:
                print 'processing link {0} of {1}'.format(count, len(links))

            if self._company_id == '23': #special handling: liberty mutual 
                if links[i].get('onclick') is None: #ignore pdf links
                    continue          
                else:
                    link = self._src.get_link(links[i].get('onclick'))
            else:                
                link = self._src.get_link(links[i].get('href'))

            if link is None: #special handling (target) 
                continue

            if link.find('External.File') > -1: #ignore links to pdfs
                continue 

            title = self._src.get_title(titles[i]).strip().encode('utf-8')
            title = title.replace('\r\n', ' ') 
            title = title.replace('\n', ' ') 
            title = title.replace('  ', ' ') 

            date = self._src.get_date(dates[i])
            if date is None:
                date = datetime.date(2012, 1, 1) #don't forget to check for these when loading!

            if date > datetime.date(2011,12,31) and date < datetime.date(2013,1,1):
                self._count += 1            
                self._sb.append('LOTW-ID: {0}\n'.format(self._count))
                self._sb.append('LOTW-DATE: {0}\n'.format(date.isoformat()))
                self._sb.append('LOTW-TITLE: {0}\n'.format(title))
                self._sb.append('LOTW-URL: {0}\n'.format(link))
                self._sb.append('\n')

                if not self._istest:
                    self._save_html(link)


    def _save_html(self, link):
        html = urlopen(link).read()
        path = os.path.join(self._path_dir, str(self._count))
        with open(path, 'w') as f:
            f.write(html)
