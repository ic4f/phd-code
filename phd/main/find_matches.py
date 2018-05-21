import sys
from data.subsets import SubsetLoader
from data.matches import MatchLoader
from analyze.match_finder import MatchFinder

def main():
    if len(sys.argv) < 7:
        raise Exception('Missing args: company_id, input_name, input_type, required_length, min_length, output_name')

    company_id = int(sys.argv[1])
    input_name = sys.argv[2]
    input_type = sys.argv[3]
    required_length = int(sys.argv[4])
    min_length = int(sys.argv[5])
    output_name = sys.argv[6]
    blocks_name_toignore = sys.argv[7]
    
    if input_type == 's':
        sloader = SubsetLoader(input_name)
        release_ids = sloader.get_pr_idset(company_id)
        article_ids = sloader.get_news_idset(company_id)
    elif input_type == 'm':
        mloader = MatchLoader(company_id, input_name)
        release_ids = mloader.get_release_ids()
        article_ids = mloader.get_article_ids()

    mf = MatchFinder(company_id, release_ids, article_ids, required_length, min_length, blocks_name_toignore)
    mf.find_matches(output_name)
    

if __name__ == '__main__': main()
