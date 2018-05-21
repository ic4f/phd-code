import sys
import os.path
from operator import itemgetter
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from data.tokens import TokenLoader
from data.matches import MatchLoader
from shared.config import ConfigReader 
from shared import common

POS_IN_BLOCK_ART = 0
POS_IN_BLOCK_REL = 1

TIME_DELTA = 14


class MatchWriter(object):

    def __init__(self, company_id, matches_name):
        self._company_id = company_id
        self._matchloader = MatchLoader(company_id, matches_name)
        self._tokens = TokenLoader(company_id)
        self._releases = ReleaseLoader(company_id).get_releases()
        self._articles = ArticleLoader(company_id).get_articles()
        self._br = ConfigReader().get('MARKER_BR')
        
    def write_matches(self, output_path):
        html = self._build_html()
        filename = '{0}.html'.format(self._company_id)
        filepath = os.path.join(output_path, filename)
        self._write_html_to_file(filepath, html) 


    def _build_html(self):
        sb = []
        counter = 0
        releases = self._get_sorted_releases()

        for release in releases:
            self._write_release_header(sb, release)
            articles = self._get_sorted_articles(release.id())

            for article in articles:
                #condition for id=35/32 only
                if self._company_id == '35':
                    delta = article.date() - release.date()
                    if delta.days >= TIME_DELTA and \
                            not (release.id() == 246 and article.id() == 944) and \
                            not (release.id() == 189 and article.id() == 1213) and \
                            not (release.id() == 71 and article.id() == 2557):
                        continue

                if self._company_id == '32':
                    delta = article.date() - release.date()
                    if delta.days >= TIME_DELTA:
                        continue

                blocks = self._matchloader.get_matches(release.id(), article.id())
                
                self._write_article_summary(sb, blocks, release, article)
                self._write_texts(sb, blocks, release.id(), article.id())
                counter += 1

        print '{0}'.format(counter)
        return ''.join(sb)


    def _get_sorted_releases(self):
        ids = self._matchloader.get_release_ids()
        rels = [self._releases[id] for id in ids]
        rels.sort(key = lambda x: x.date())
        return rels

    def _get_sorted_articles(self, release_id):
        ids = self._matchloader.get_article_ids(release_id)
        arts = [self._articles[id] for id in ids]
        arts.sort(key = lambda x: x.date())
        return arts

    def _write_release_header(self, sb, release):
        sb.append('\n\t<tr>\n\t\t<td colspan="2" class="release-title">')
        sb.append('{0} --- {1} --- {2}\n\t\t</td>\n\t</tr>'.format( \
                release.id(), release.date().strftime('%B %d'), release.title()))


    def _write_article_summary(self, sb, blocks, release, article):
        sb.append('\n\t<tr><td colspan=2>')
        sb.append('\n\t\t<table class="tbl-inner1" cellpadding="5" border="1"i>')

        sb.append('\n\t\t\t<tr class="tbl-inner1-title"><td colspan="3" class="article-title">')
        sb.append('R: {0} --- {1} --- {2}\n\t\t</td>\n\t</tr>'.format( \
                release.id(), release.date().strftime('%B %d'), release.title()))
        
        sb.append('\n\t\t\t<tr class="tbl-inner1-title"><td colspan="3" class="article-title">')
        sb.append('A: {0} --- {1} --- {2} --- {3}\n\t\t</td>\n\t</tr>'.format( \
                article.id(), article.date().strftime('%B %d'), article.headline(), article.pub()))

        sb.append('\n\t\t\t<tr class="tbl-inner1-title"><td>#</td><td>length</td><td>match</td></tr>')

        for count, block in enumerate(blocks):
            i = block[0] #start in article
            j = block[1] #start in release
            k = block[2] #length
        
            rel_match = self._tokens.get_stripped_release_token_block(release.id(), j,j+k)
            art_match = self._tokens.get_stripped_article_token_block(article.id(), i,i+k)
            
            rel_temp = ' '.join(rel_match)
            art_temp = ' '.join(art_match)
                        
            rel_temp = rel_temp.replace(self._br, ' ')
            art_temp = art_temp.replace(self._br, ' ')

            if rel_temp.lower() != art_temp.lower():
                print rel_temp.lower()
                print art_temp.lower()
                raise Exception("blocks don't match")

            sb.append('\n\t\t\t<tr valign="top">')
            sb.append('\n\t\t\t\t<td>{0}</td>'.format(count+1))
            sb.append('\n\t\t\t\t<td>{0}</td>'.format(k))
            sb.append('\n\t\t\t\t<td><span class="match match{0}">{1}</span>\n\t\t</td>'.format(count, rel_temp))
            sb.append('\n\t\t\t</tr>')

        sb.append('\n\t\t</table>')
        sb.append('\n\t</td></tr>')


    def _write_texts(self, sb, blocks, release_id, article_id):
        rel_tokens = self._tokens.get_release_tokens(release_id, False)
        art_tokens = self._tokens.get_article_tokens(article_id, False)
        rel_html = self._get_text(blocks, rel_tokens, POS_IN_BLOCK_REL)
        art_html = self._get_text(blocks, art_tokens, POS_IN_BLOCK_ART)

        sb.append('\n\t<tr valign="top">')
        sb.append('\n\t\t<td width="50%">{0}\n\t\t</td>'.format(rel_html))
        sb.append('\n\t\t<td width="50%">{0}\n\t\t</td>'.format(art_html))
        sb.append('\n\t</tr>')


    def _get_text(self, blocks, orig_tokens, pos_in_block):
        span_start = '<span class="match match{0}">'
        span_end = '</span>'
        #clone list
        tokens = orig_tokens[:]

        #sort by position in article
        blocks = sorted(blocks, key=itemgetter(pos_in_block))       
        a = 0
        for count, block in enumerate(blocks):
            pos = block[pos_in_block] #position in text
            k = block[2] #length

            tokens.insert(pos+a, span_start.format(count))
            tokens.insert(pos+k+a+1, span_end)
            a += 2

        html = ' '.join(tokens)
        html = html.replace(self._br, '<br/>')
        return html
   

    def _write_html_to_file(self, output_path, html):
        with open(output_path, 'w') as f:
            f.write('<html>\n<head>')
            f.write('\n\t<link rel="stylesheet" type="text/css" href="styles.css">')
            f.write('\n</head>\n<body>\n')
            f.write('\n<table class="tbl-main" cellpadding="5" border="1">')
            f.write(html)
            f.write('\n</table>')
            f.write('\n\n</body>\n</html>')
