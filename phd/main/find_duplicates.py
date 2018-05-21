import sys
from analyze.duplicate_finder import DuplicateFinder

def main():
    company_id = int(sys.argv[1])
    DuplicateFinder(company_id).find_release_duplicates()


if __name__ == '__main__': main()
