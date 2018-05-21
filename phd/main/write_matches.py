import sys
from analyze.match_writer import MatchWriter

# Required args: company_id, output_path
def main():
    company_id = sys.argv[1]
    matches_name = sys.argv[2]
    output_path = sys.argv[3]

    mw = MatchWriter(company_id, matches_name)
    mw.write_matches(output_path)


if __name__ == '__main__': main()
