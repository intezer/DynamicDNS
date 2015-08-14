import argparse
import csv

class dyndns(object):
    def __init__(self):
        try:
            self.dyndns = {}
            with open('dynamic-dns.csv') as f:
                reader = csv.DictReader(f) 
                for row in reader:
                    self.dyndns[row["domain"]] = row["comment"]
            self.dyndns.pop('m', None)
        except:
            print "Failure loading dyndns database"
            raise
    def correlate(self, domain_list):
        results = []
        for domain in domain_list:
            for dyndns_domain in self.dyndns.iterkeys():
                if domain.endswith('.' + dyndns_domain):
                   results.append([domain, dyndns_domain, self.dyndns[dyndns_domain]])
                   break
        return results
                
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-f', '--file', default=None, help="Text file with domains seperated by new line")
    parser.add_argument('-o', '--output', default="dyndns_output.csv", help="Output filename")
    args = parser.parse_args()
    
    # Read domains to correlate
    domains = open(args.file).read().splitlines() 

    dyn = dyndns()
    results = dyn.correlate(domains)

    # Output
    with open(args.output, 'wb') as outputfile:
        wr = csv.writer(outputfile, quoting=csv.QUOTE_ALL)
        wr.writerow(["domain", "dyndns_domain", "dyndns_comment"])
        for result in results:
            wr.writerow(result)
