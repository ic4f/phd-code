import sys
from data.matches import MatchLoader
from analyze.sentence_writer import SentenceWriter

def main():
    company_id = int(sys.argv[1])
    input_name = sys.argv[2]
    output_name = sys.argv[3]
   
    for company_id in range(21, 41):
        print 'PROCESSING COMPANY {0}'.format(company_id)

        mloader = MatchLoader(company_id, input_name)
        release_ids = mloader.get_release_ids()
        article_ids = mloader.get_article_ids()

        sw = SentenceWriter(company_id, release_ids, article_ids, output_name)
        sw.write_and_calculate()


if __name__ == '__main__': main()
