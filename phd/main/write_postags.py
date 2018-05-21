import sys
from analyze.postag_writer import POSTagWriter

def main():
    matches_name = sys.argv[1]

    for company_id in range(21, 41):
        print 'PROCESSING COMPANY {0}'.format(company_id)
        pt = POSTagWriter()
        pt.write_tags(matches_name, company_id)


if __name__ == '__main__': main()
