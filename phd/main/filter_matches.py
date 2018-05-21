import sys
from analyze.match_filter import MatchFilter

def main():
    company_id = sys.argv[1]
    matches_name_in = sys.argv[2]
    matches_name_out = sys.argv[3]
#    pairs_name = sys.argv[4]
    min_len = int(sys.argv[4])

    mf = MatchFilter(company_id, matches_name_in, matches_name_out)
#    mf.filter_exclude_pairs(pairs_name)
    mf.filter_by_min_len(min_len)


if __name__ == '__main__': main()
