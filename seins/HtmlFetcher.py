__author__ = 'mackaiver'
import time
import requests
import logging

logger = logging.getLogger('root')


class HtmlFetcher:
    #take departure and arrival location and optinaly departure day and time
    def get_efa_html(self, dep, arr, day=None, departure_time=None):
        raise NotImplementedError


class DBHtmlFetcher(HtmlFetcher):
    _url = 'http://mobile.bahn.de/bin/mobil/query2.exe/dox'

    def get_efa_html(self, dep, arr, day=None, departure_time=None):
        if not day:
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