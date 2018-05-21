import sys
from analyze.block_finder import BlockFinder

# Required args: company_id, output_path
def main():
    company_id = int(sys.argv[1])
    matches_name = sys.argv[2]
    min_len = int(sys.argv[3])
   
    if len(sys.argv) == 4:
        max_len = sys.maxint
    else:
        max_len = int(sys.argv[4])

    bf = BlockFinder(company_id, matches_name)
    #bf.print_all_matching_blocks(min_len, max_len)
    bf.print_all_nondiscrim_release_blocks(min_len, max_len)


if __name__ == '__main__': main()
