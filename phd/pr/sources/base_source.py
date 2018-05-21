from bs4 import BeautifulSoup, Comment


class BaseSource(object):

    def _filter_html(self, html):
        soup = BeautifulSoup(html)
        tags = soup.find_all('table')
        if len(tags) > 0:
            for t in tags:
                t.clear()

        tags = soup.find_all('style')
        if len(tags) > 0:
            for t in tags:
                t.clear()

        comments = soup.findAll(text=lambda text:isinstance(text, Comment))
        [comment.extract() for comment in comments]
        return soup.get_text()
