import sys
from pr.formatter import Formatter

# Required args: company_id, output_path
def main():
    if len(sys.argv) < 3:
        raise Exception('Missing args: company_id, output_path')
    
    company_id = sys.argv[1]
    output_path = sys.argv[2]
    Formatter(company_id, output_path).run()


if __name__ == '__main__': main()
