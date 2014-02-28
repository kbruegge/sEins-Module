# -*- coding: utf-8 -*-
__author__ = 'mackaiver'

#Lets start with a simple commandline tool
import argparse
import requests
import os

from bs4 import BeautifulSoup
import time

from colorama import init, Fore, Style
#init colorama so it works on windows as well. The autoreset flag keeps me from using RESET on each line I want to color
init(autoreset=True)

import logging
#create a logger for this module
logger = logging.getLogger(__name__)
#use colorama codes to color diferent output levels
logging.addLevelName(logging.WARNING, Style.BRIGHT + Fore.YELLOW +
                                      logging.getLevelName(logging.WARNING) + Style.RESET_ALL)
logging.addLevelName(logging.ERROR, Style.BRIGHT + Fore.RED + logging.getLevelName(logging.ERROR) + Style.RESET_ALL)
#the usual formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create a handler and make it use the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
# now tell the logger to use the handler
logger.addHandler(handler)


class Fetcher:
    url = 'http://mobile.bahn.de/bin/mobil/query2.exe/dox'

    def create_time_and_date(self):
        #returns time and then day
        return time.strftime("%H:%M"), time.strftime("%d.%m.%Y")

    def get_efa(self, dep, arr, day=None, time=None):
        if day is None or time is None:
            time, day = self.create_time_and_date()

        payload = {'REQ0HafasOptimize1': '0:1',
                   'REQ0HafasSearchForw': '1',
                   'REQ0JourneyStopsS0A': '1',
                   'REQ0JourneyDate': day,
                   'REQ0JourneyStopsS0G': dep,
                   'REQ0JourneyStopsS0ID': None,
                   'REQ0JourneyStopsZ0A': '1',
                   'REQ0JourneyStopsZ0G': arr,
                   'REQ0JourneyStopsZ0ID': None,
                   'REQ0JourneyTime': time,
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


class DBPage:
    _html = None
    _soup = None
    _errormessages = []
    _trains = []

    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html)
        logger.debug(self._soup.prettify())
        self.get_errors()
        self._parse_trains_()

    def get_errors(self):
        if self._errormessages:
            return self._errormessages

        self._errormessages = self._soup.find_all('div', 'errormsg')
        return self._errormessages

    def _parse_trains_(self):
        trains = []
        arrivals = self._soup.select("tr.ovConLine")
        for t in arrivals:
            trains.append(self._parse_row(t))
        s_trains = [el for el in trains if el[2] == 'S' or el[2] == 'S ']
        print(str(s_trains))
        return True

    def _parse_row(self, row):
        #print(str(row))
        cell1 = row.select("td.timelink  a")
        arr = None
        delay = None
        traintype = None

        if cell1:
            arr = cell1[0].text
        cell2 = row.select("td.tprt  span")
        if cell2:
            delay = cell2[0].text
        cell3 = row.select("td.iphonepfeil")
        if cell3:
            traintype = cell3[0].text

        return arr, delay, traintype

    def print_errors(self):
        for r in self._errormessages:
            logger.error('Webpage raised an error: ' + r.getText())


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

    (output_path, departure, arrival) = parse_args()
    fetcher = Fetcher()
    resp = fetcher.get_efa(departure, arrival)
    page = DBPage(resp)
    if page.get_errors():
        page.print_errors()

    if output_path is None:
        logger.info('REsponse from server was: ')
        print(resp)
    else:
        with open(output_path, 'wt') as file:
            file.write(resp)
            logger.info(Fore.GREEN + "Output written to " + output_path)



