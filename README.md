# Ph.D. dissertation research code

> **This project is deprecated and not maintained. It exists for historical reasons only.**

This is the code I wrote for my Ph.D. dissertation at the University of Maryland (2012). It is primarily
large-scale text reuse detection with basic sentiment analysis. It was used to construct a large
data set containing press releases and related news coverage and analyze the relationship between
these two groups. The results of the data analysis were used to challenge an existing social
scientific theory. 


## What this code does

Some of the the data collection and processing steps included:
- crawl a predetermined set of websites and extract relevant data from online newsrooms 
- extract news articles from LexisNexis bulk downloads
- tokenize the corpus; identify instances of matching sequences of n tokens appearing in a press
  release and one or more news articles
- eliminate bad discriminators (non-unique token sequences appearing in more than one press release - 
  i.e., corporate boilerplate doesn't help identify a relationship between a release and an
  article)
- run a sentence tokenizer + part-of-speech tagger; then attempt to match each token against a
  subjectivity lexicon; calculate document subjectivity and polarity scores 
-  ...and many more routine and ad-hoc data cleaning and processing tasks


## Related

* My dissertation is <a href="https://drum.lib.umd.edu/handle/1903/14638">available here</a>.
* A browsable HTML version of the constructed dataset (including all identified instances of text
  reuse + extracted quotes) is <a href="http://sergey.cs.uni.edu/phd">available here</a>. 
  (<a href="http://sergey.cs.uni.edu/phd/matches/37.html">Here's a sample</a>)
* My <a href="http://sergey.cs.uni.edu/phd/defense.pdf">defense slide deck</a> is a brief overview of the dissertation. 
* Here's <a href="http://sergey.cs.uni.edu/phd/fellowship.pdf">another slide deck</a> from a follow-up study on a larger data set.

## Disclaimer 
This is dissertation research code: it is neither elegant, nor reusable. It doesn't follow PEP 8
very closely. It is messy, suboptimal, and occasionally incomprehensible. It was written for Python
2, and it won't run under Python 3. More importantly, web scrapers are short-lived by definition; I
doubt any of the scrapers in this codebase are still usable on their respective target websites.


## License
[MIT](https://github.com/ic4f/phd-code/blob/master/LICENSE)
