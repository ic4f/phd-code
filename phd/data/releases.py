import os.path
import datetime
from shared import common
from shared.config import ConfigReader


class ReleaseLoader(object):

    def __init__(self, company_id):
        self._releases = {}
        self._load(company_id)

    def get_releases(self):
        return self._releases

    def _load(self, company_id):
        cfr = ConfigReader()
        p1 = cfr.get('ROOT_ORIGINAL')
        p2 = cfr.get('FORMATTED_PR')
        p3 = os.path.join(p1, p2)
        metafile = common.get_list_file_name(company_id)

        path_text = os.path.join(p3, str(company_id))
        path_meta = os.path.join(p3, metafile)

        pr_text = self._load_text(path_text)
        self._load_meta(path_meta, pr_text)

    def _load_text(self, path):
        text = {}
        release_id = -1
        sb = []
        with open(path) as f:
            while True:
                line = f.readline()
                if line == '':
                    text[release_id] = ''.join(sb) #flush last record
                    break
                if line.startswith('LOTW-ID: '):
                    if release_id != -1:
                        text[release_id] = ''.join(sb)
                    release_id = int(line[9:].strip())
                    sb = []
                else:
                    sb.append(line)
        return text

    def _load_meta(self, path, pr_text):
        release_id = -1
        with open(path) as f:
            while True:
                line = f.readline()
                if line == '':
                    self._releases[release_id] = Release(release_id, date, title, url, pr_text[release_id])
                    break
                if line.startswith('LOTW-ID: '):
                    if release_id != -1:
                        self._releases[release_id] = Release(release_id, date, title, url, pr_text[release_id])
                    release_id = int(line[9:].strip())
                elif line.startswith('LOTW-DATE: '):
                    date = line[11:]
                elif line.startswith('LOTW-TITLE: '):
                    title = line[12:]
                elif line.startswith('LOTW-URL: '):
                    url = line[10:]


class Release(object):

    def __init__(self, release_id, date, title, url, body):
        self._releases = release_id, self._load_date(date), title, url, body

    def id(self):
        return self._releases[0]

    def date(self):
        return self._releases[1]

    def title(self):
        return self._releases[2]
                
    def url(self):
        return self._releases[3]
                
    def body(self):
        return self._releases[4]
                
    def _load_date(self, date):
        date = date.strip()
        return datetime.datetime.strptime(date, '%Y-%m-%d') 
