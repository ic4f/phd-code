import sys
from data.subsets import SubsetLoader
from data.matches import MatchLoader
from analyze.text_writer import TextWriter

def main():
    company_id = int(sys.argv[1])
    input_name = sys.argv[2]
    input_type = sys.argv[3]
    output_name = sys.argv[4]
    
    if input_type == 'm':
        mloader = MatchLoader(company_id, input_name)
        release_ids = mloader.get_release_ids()
        article_ids = mloader.get_article_ids()

    tw = TextWriter(company_id, release_ids, article_ids, output_name)
    tw.write()


if __name__ == '__main__': main()
