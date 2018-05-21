import re
from shared import common
from data.releases import ReleaseLoader


def find_quotes():
    p = re.compile('"[^"]+"')

    for i in range(1, 41):
        i = str(i)
        print 'Processing company {0}'.format(i)
        output_path = common.get_quotes_path(i) 
        releases = ReleaseLoader(i).get_releases()
        all_quotes = []

        for rid in releases:
            release = releases[rid]
            quotes = p.findall(release.body())
            all_quotes += quotes

        with open(output_path, 'w') as f:
            for q in all_quotes:
                q = q.replace('\n', '')
                if len(q) > 50 and len(q) < 300:
                    f.write(q + '\n\n')

