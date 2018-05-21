#this is just a driver for testing stuff
import sys
from data.releases import ReleaseLoader
from data.articles import ArticleLoader
from data.subsets import SubsetLoader
from data.tokens import TokenLoader
from data.matches import MatchLoader
from data.blocks import BlockLoader
from data.duplicates import DuplicateLoader
from data.pairs import PairLoader
from data.subjlexicon import SubjLexiconLoader
from analyze.subjlex_finder import SubjlexFinder
from data.postags import POSTagLoader
from data.scores import ScoreLoader
from analyze.match_finder import MatchFinder

def main():
#uncomment as needed:
#    test_subsetloader()
#    test_releaseloader()
#    test_articleloader()
#    test_tokenloader()
#    test_matchloader()
#    test_matchloader_forall()
#    test_blockloader()
#    test_duplicateloader()
#    test_pairloader()
#    test_subjlexiconLoader()
#    test_subjlexFinder()
#    test_postagLoader()
#    test_scoreLoader()
    test_mics()
    pass

def test_mics():
    release_ids = [60]
    article_ids = [664]
    m = MatchFinder(28, release_ids, article_ids, 7, 7, None)
    m.find_matches(None)

def test_subsetloader():
    company_id = int(sys.argv[1])
    s = SubsetLoader('all')
    print 'Testing SubsetLoader'
    print 'company-id: {0}'.format(company_id)
    print 'releases: {0}'.format(len(s.get_pr_idset(company_id)))
    print 'artciles {0}'.format(len(s.get_news_idset(company_id)))

def test_releaseloader():
    company_id = int(sys.argv[1])
    r = ReleaseLoader(company_id)
    print 'Testing ReleaseLoader'
    print 'company-id: {0}'.format(company_id)
    print 'releases: {0}'.format(len(r.get_releases()))

def test_articleloader():
    company_id = int(sys.argv[1])
    a = ArticleLoader(company_id)
    print 'Testing ArticleLoader'
    print 'company-id: {0}'.format(company_id)
    print 'articles: {0}'.format(len(a.get_articles()))

def test_tokenloader():
    company_id = int(sys.argv[1])
    t = TokenLoader(company_id)
    r = ReleaseLoader(company_id)
    a = ArticleLoader(company_id)
        
    print 'Testing TokenLoader'
    print 'company-id: {0}'.format(company_id)

    articles = a.get_articles()
    article_id = articles.itervalues().next().id()
    print 'article-id: {0}'.format(article_id)
    print 'TOKENS:'
    print t.get_article_tokens(article_id, False)

    releases = r.get_releases()
    release_id = releases.itervalues().next().id()
    print 'release-id: {0}'.format(release_id)
    print 'TOKENS:'
    print t.get_release_tokens(release_id, False)

def test_matchloader():
    company_id = int(sys.argv[1])
    matches_name = sys.argv[2]
    m = MatchLoader(company_id, matches_name) 
    print 'Testing MatchLoader'
    print 'company-id: {0}'.format(company_id)
    print 'releases: {0}'.format(len(m.get_release_ids()))
    print 'articles: {0}'.format(len(m.get_article_ids()))
    print 'pairs: {0}'.format(m.count_rel_art_pairs())
    print 'blocks: {0}'.format(m.count_matching_blocks())

def test_matchloader_forall():
    matches_name = sys.argv[1]

    for id in range(1, 41):
        m = MatchLoader(id, matches_name) 
#        print '{0}'.format(len(m.get_release_ids()))
#        print '{0}'.format(len(m.get_article_ids()))
#        print '{0}'.format(m.count_rel_art_pairs())
        print '{0}'.format(m.count_matching_blocks())

def test_blockloader():
    company_id = int(sys.argv[1])
    blocks_name = sys.argv[2]
    b = BlockLoader(company_id, blocks_name)
    print 'Testing BlockLoader'
    print 'company-id: {0}'.format(company_id)
    blocks = b.get_blocks()
    print 'BLOCKS: {0}'.format(len(blocks))
    for b in blocks:
        print b

def test_duplicateloader():
    company_id = int(sys.argv[1])
    duplicates = DuplicateLoader(company_id)
    releases = ReleaseLoader(company_id).get_releases()
    articles = ArticleLoader(company_id).get_articles()
    print 'Testing DuplicateLoader'
    print 'company-id: {0}'.format(company_id)

    rel_dups = duplicates.get_release_duplicates()
    print 'RELEASE DUPLICATES: {0}'.format(len(rel_dups))
    for d in rel_dups:
        r = releases[int(d)]
        print '{0} : {1}'.format(r.id(), r.title())

    art_dups = duplicates.get_article_duplicates()
    print 'ARTICLE DUPLICATES: {0}'.format(len(art_dups))
    for d in art_dups:
        a = articles[int(d)]
        print '{0} : {1}'.format(a.id(), a.headline())

def test_pairloader():
    company_id = 12 # hardcoded
    pairs_name = sys.argv[1]
    ploader = PairLoader(company_id, pairs_name)
    print 'Testing PairLoader'
    print 'company-id: {0}'.format(company_id)
    pairs = ploader.get_pairs()
    print 'PAIRS: {0}'.format(len(pairs))
    for p in pairs:
        print p

    #true:
    rel1 = 23
    art1 = 964
    print '{0}-{1} in pairs: {2}'.format(rel1, art1, ploader.has_pair(rel1, art1))

    #false:
    rel2 = 23
    art2 = 965
    print '{0}-{1} in pairs: {2}'.format(rel2, art2, ploader.has_pair(rel2, art2))

def test_subjlexiconLoader():
    sloader = SubjLexiconLoader()
    print sloader.get_polarity(sys.argv[1], sys.argv[2])

def test_subjlexFinder():
    company_id = int(sys.argv[1])
    slfinder = SubjlexFinder(company_id)
    slfinder.run()

def test_postagLoader():
    company_id = int(sys.argv[1])
    name = sys.argv[2]
    tloader = POSTagLoader(company_id, name)
    print tloader.get_release_tags(34)

def test_scoreLoader():
    company_id = 9
    scores = ScoreLoader(company_id)

    print scores.count_pos_rel_sentences(161)
    print scores.count_neg_rel_sentences(161)
    print scores.count_posneg_rel_sentences(161)
    print scores.count_subj_rel_sentences(161)
    print scores.count_all_rel_sentences(161)
    print scores.count_pos_rel_words(161)
    print scores.count_neg_rel_words(161)
    print ''
    print scores.count_pos_art_sentences(277)
    print scores.count_neg_art_sentences(277)
    print scores.count_posneg_art_sentences(277)
    print scores.count_subj_art_sentences(277)
    print scores.count_all_art_sentences(277)
    print scores.count_pos_art_words(277)
    print scores.count_neg_art_words(277)


if __name__ == '__main__': main()
