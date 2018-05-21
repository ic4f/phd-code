import sys
from analyze.token_writer import TokenWriter

# Required args: company_id
def main():
    if len(sys.argv) < 2:
        raise Exception('Missing args: company_id')

    company_id = sys.argv[1]
    tw = TokenWriter()
    tw.write_tokens(company_id)


if __name__ == '__main__': main()
