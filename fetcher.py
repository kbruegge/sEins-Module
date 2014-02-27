# -*- coding: utf-8 -*-
__author__ = 'mackaiver'

#Lets start with a simple commandline tool

import argparse
import urllib.request
import os
from colorama import init, Fore

init()


class Fetcher:
    #url = 'http://mobile.bahn.de/bin/mobil/query2.exe/dox'
    url = 'http://mobile.bahn.de/bin/mobil/query.exe/dox?ld=9647&rt=1&use_realtime_filter=1&OK#focus'

    def get_efa(self, departure, arrival):
        values = {'REQ0HafasOptimize1': '0:1',
                  'REQ0HafasSearchForw': '1',
                  'REQ0JourneyDate': '27.02.14',
                  'REQ0JourneyStopsS0A': '1',
                  'REQ0JourneyStopsS0G': 'universitaet s-bahnhof, dortmund',
                  'REQ0JourneyStopsS0ID': None,
                  'REQ0JourneyStopsZ0A': '1',
                  'REQ0JourneyStopsZ0G': 'dortmund hbf',
                  'REQ0JourneyStopsZ0ID': None,
                  'REQ0JourneyTime': '16:00',
                  'REQ0Tariff_Class': '2',
                  'REQ0Tariff_TravellerReductionClass.1': '0',
                  'REQ0Tariff_TravellerType.1': 'E',
                  'existOptimizePrice': '1',
                  'immediateAvail': 'ON',
                  'queryPageDisplayed': 'yes',
                  'start': 'Suchen'}

        data = urllib.parse.urlencode(values)
        data = data.encode('ascii')  # data should be bytes

        req = urllib.request.Request(self.url, data)
        response = urllib.request.urlopen(req)
        return response.read().decode('utf-8')


def is_valid_file(parser, arg):
    (folder, t) = os.path.split(arg)
    print(os.path.split(arg))

    if not folder == '' and not os.path.exists(folder):
        parser.error("The folder %s does not exist!" % folder)
    else:
        return arg


if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Lecker data fetching from EFA via the commandline. ',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('-d', default='Universität s-Bahnhof, Dortmund', metavar='--from', type=str,
                   help='Name of the departing station')
    p.add_argument('-a', default='Dortmund hbf', metavar='--to', type=str, help='Name of the arrival station')

    p.add_argument('-o', metavar='--output', type=lambda path: is_valid_file(p, path), help='path to outputfile')

    args = p.parse_args()
    f = Fetcher()
    resp = f.get_efa(args.d, args.a)
    if 'eindeutig' in resp:
        print(Fore.RED + 'Eingabe nicht eindeutig' + Fore.RESET)

    if args.o is None:
        print(resp)
    else:
        with open(args.o, 'wt') as file:
            file.write(resp)
            print("Output written to " + args.o)



