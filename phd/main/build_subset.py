import sys
from analyze.subset_builder import SubsetBuilder

# Required args: subset_name
def main():
    sb = SubsetBuilder()
    sb.build_subset_all()


if __name__ == '__main__': main()
