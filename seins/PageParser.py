__author__ = 'mackaiver'

from bs4 import BeautifulSoup
from seins.HtmlFetcher import DBHtmlFetcher


class DBWebError(Exception):
    def __init__(self, messages):
        self.messages = messages


class PageParser:
    _html = None
    _soup = None

    def __init__(self, dep, arr, day=None, departure_time=None):
        fetcher = DBHtmlFetcher()
        self._html = fetcher.get_efa_html(dep, arr, day, departure_time)
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
    def from_html(cls, html):
        cls._html = html
        cls._soup = BeautifulSoup(cls._html)
        cls._parse_soup()

    @classmethod
    def from_html_fetcher(cls, fetcher, dep, arr, day=None, departure_time=None):
        cls._html = fetcher.get_efa_html(dep, arr, day, departure_time)
        cls._soup = BeautifulSoup(cls._html)
        cls._parse_soup()

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
