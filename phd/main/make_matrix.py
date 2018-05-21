import sys
from analyze.matrix_maker import MatrixMaker

def main():
    matches_name = sys.argv[1]

    mm = MatrixMaker(matches_name)
#    mm.print_matrix()
    mm.print_pairs()


if __name__ == '__main__': main()
