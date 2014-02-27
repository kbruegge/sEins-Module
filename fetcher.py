# -*- coding: utf-8 -*-
__author__ = 'mackaiver'

#Lets start with a simple commandline tool

import argparse
import requests
import os
from colorama import init, Fore

init(autoreset=True)

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)


class Fetcher:
    url = 'http://mobile.bahn.de/bin/mobil/query2.exe/dox'

    def get_efa(self, dep, arr):
        payload = {'REQ0HafasOptimize1': '0:1',
                   'REQ0HafasSearchForw': '1',
                   'REQ0JourneyStopsS0A': '1',
                   'REQ0JourneyDate': '27.02.14',
                   'REQ0JourneyStopsS0G': dep,
                   'REQ0JourneyStopsS0ID': None,
                   'REQ0JourneyStopsZ0A': '1',
                   'REQ0JourneyStopsZ0G': arr,
                   'REQ0JourneyStopsZ0ID': None,
                   'REQ0JourneyTime': '17:58',
                   'REQ0Tariff_Class': '2',
                   'REQ0Tariff_TravellerReductionClass.1': '0',
                   'REQ0Tariff_TravellerType.1': 'E',
                   'existOptimizePrice': '1',
                   'immediateAvail': 'ON',
                   'queryPageDisplayed': 'yes',
                   'start': 'Suchen'}

        r = requests.post(self.url, data=payload)
        logger.debug(r.text)
        return r.text


def is_valid_file(parser, arg):
    (folder, t) = os.path.split(arg)
    #logger.debug('given path is:' + os.path.split(arg))

    if not folder == '' and not os.path.exists(folder):
        parser.error("The folder %s does not exist!" % folder)
    else:
        return arg


def parse_args():
    p = argparse.ArgumentParser(description='Lecker data fetching from EFA via the commandline. ',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('-d', default='Universität s-Bahnhof, Dortmund', metavar='--from', type=str,
                   help='Name of the departing station')
    p.add_argument('-a', default='Dortmund hbf', metavar='--to', type=str, help='Name of the arrival station')

    p.add_argument('-o', metavar='--output', type=lambda path: is_valid_file(p, path), help='path to outputfile')
    p.add_argument('-v', action="store_true", help='Show some nice debug output')

    args = p.parse_args()
    #check for debug logging
    if args.v:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    return args.o, args.d, args.a


if __name__ == '__main__':

    (output, departure, arrival) = parse_args()
    fetcher = Fetcher()
    resp = fetcher.get_efa(departure, arrival)
    if 'eindeutig' in resp:
        logger.warning(Fore.RED + 'Eingabe nicht eindeutig')

    if output is None:
        logger.info('REsponse from server was: ')
        print(resp)
    else:
        with open(output, 'wt') as file:
            file.write(resp)
            logger.info("Output written to " + output)



