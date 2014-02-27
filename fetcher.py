__author__ = 'mackaiver'

#Lets start with a simple commandline tool

import argparse
import urllib.request


class Fetcher:
    url = 'http://mobile.bahn.de/bin/mobil/query2.exe/dox'

    def get_efa(self, departure, arrival):
        response = urllib.request.urlopen(self.url)
        data = response.read()
        print(data)


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Lecker data fetching from EFA via the commandline. ',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('-d', default='Universität s-Bahnhof, Dortmund', metavar='from', type=str,
                   help='Name of the departing station')
    p.add_argument('-a', default='Dortmund hbf', metavar='to', type=str, help='Name of the arrival station')

    args = p.parse_args()
    f = Fetcher()
    f.get_efa(args.d, args.a)


