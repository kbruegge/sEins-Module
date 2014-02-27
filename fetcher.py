__author__ = 'mackaiver'

#Lets start with a simple commandline tool

import argparse

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Lecker data fetching from EFA via the commandline. ')

    p.add_argument('from', default='Universität s-Bahnhof, Dortmund', metavar='from', type=str,
                   help='Name of the departing station')
    p.add_argument('to', default='Dortmund hbf', metavar='to', type=str, help='Name of the arrival station')

    args = p.parse_args()
    print(args)
