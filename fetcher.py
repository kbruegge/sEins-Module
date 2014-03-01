# -*- coding: utf-8 -*-
__author__ = 'mackaiver'

#Lets start with a simple commandline tool
import argparse
import requests
import os

from bs4 import BeautifulSoup
import time

from colorama import init, Fore, Style
#init colorama so it works on windows as well.
#The autoreset flag keeps me from using RESET on each line I want to color
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


class HtmlFetcher:
    #take departure and arrival location and optinaly departure day and time
    def get_efa_html(self, dep, arr, day=None, departure_time=None):
        raise NotImplementedError


class DBHtmlFetcher(HtmlFetcher):
    _url = 'http://mobile.bahn.de/bin/mobil/query2.exe/dox'

    def get_efa_html(self, dep, arr, day=None, departure_time=None):
        if not day :
            day = time.strftime("%d.%m.%Y")

        if not departure_time:
            departure_time = time.strftime("%H:%M")

        payload = {'REQ0HafasOptimize1': '0:1',
                   'REQ0HafasSearchForw': '1',
                   'REQ0JourneyStopsS0A': '1',
                   'REQ0JourneyDate': day,
                   'REQ0JourneyStopsS0G': dep,
                   'REQ0JourneyStopsS0ID': None,
                   'REQ0JourneyStopsZ0A': '1',
                   'REQ0JourneyStopsZ0G': arr,
                   'REQ0JourneyStopsZ0ID': None,
                   'REQ0JourneyTime': departure_time,
                   'REQ0Tariff_Class': '2',
                   'REQ0Tariff_TravellerReductionClass.1': '0',
                   'REQ0Tariff_TravellerType.1': 'E',
                   'existOptimizePrice': '1',
                   'immediateAvail': 'ON',
                   'queryPageDisplayed': 'yes',
                   'start': 'Suchen'}

        r = requests.post(self._url, data=payload)
        logger.debug(r.text)
        return r.text


class DBWebError(Exception):
    def __init__(self, messages):
        self.messages = messages


class PageParser:
    _html = None
    _soup = None

    def __init__(self, dep, arr, day=None, departure_time=None):
        fetcher = DBHtmlFetcher()
        self._html = fetcher.get_efa_html(departure, arrival, day , departure_time )
        self._soup = BeautifulSoup(self._html)

    @property
    def connections(self):
        raise NotImplementedError


class DBPageParser(PageParser):
    _errormessages = []
    _connections = []

    def __init__(self, dep, arr, day=None, departure_time=None):
        super().__init__(dep, arr, day, departure_time)
        self._parse_soup()

    @classmethod
    def from_html(self, html):
        self._html = html
        self._soup = BeautifulSoup(self._html)
        self._parse_soup()

    @classmethod
    def from_html_fetcher(self, fetcher, dep, arr, day=None, departure_time=None):
        self._html = fetcher.get_efa_html(departure, arrival, day , departure_time )
        self._soup = BeautifulSoup(self._html)
        self._parse_soup()

    #returns a tuple of the form (departuretime, arrivaltime, delay, traintype)
    @property
    def connections(self):
        return self._connections

    @property
    def html(self):
        return self._html

    #returns a list of strings hopefully containng meaningfull erromessages from the webpage we parsed
    def get_errors(self):
        if self._errormessages:
            return self._errormessages

        #find all div tags with class erromsg that have soem text
        errortags = self._soup.find_all('div', 'errormsg', text=True)
        return [e.text for e in errortags]


    def _parse_soup(self):
        self._errormessages = self.get_errors()
        self._connections = self._parse_trains_()

        if self._errormessages:
            raise DBWebError(self._errormessages)


    def _parse_trains_(self):
        trains = []
        arrivals = self._soup.select("tr.ovConLine")

        for t in arrivals:
            trains.append(self._parse_row(t))

        return trains

    def _parse_row(self, row):
        #print(str(row))
        dep = None
        arr = None
        delay = None
        traintype = None

        cell1 = row.select("td.timelink  a")
        if cell1:
            dep = cell1[0].text[:5]
            arr = cell1[0].text[5:]
        cell2 = row.select("td.tprt  span")
        if cell2:
            delay = cell2[0].text
        cell3 = row.select("td.iphonepfeil")
        if cell3:
            traintype = cell3[0].text

        return dep, arr, delay, traintype


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
    #fetcher = DBHtmlFetcher()
    #resp = fetcher.get_efa(departure, arrival )
    page = DBPageParser(departure, arrival)
    print(page.connections)

    if output_path:
        with open(output_path, 'wt') as file:
            file.write(page.html)
            logger.info(Fore.GREEN + "Output written to " + output_path)



