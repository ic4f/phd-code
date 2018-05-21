import sys
from pr import crawler

# Required args: company_id, output_path
# Optional args: -t (test mode)
def main():
    if len(sys.argv) < 3:
        raise Exception('Missing args: company_id, output_path')

    id = sys.argv[1]
    path = sys.argv[2]
    cr = crawler.Crawler(id, path)
    if len(sys.argv) == 3:
        cr.run()
    elif len(sys.argv) == 4 and sys.argv[3] == '-t':
        cr.run(True)


if __name__ == '__main__': main()
