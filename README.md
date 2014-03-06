sEins
============

A small module for fetching and parsing stuff from EFA on the DBWebsite. Also provides command line utility
so you can quickly see if your train is on time or not


Command Line Usage
-------------

After doing `pip3 install sein` you can use the command line tool called `seins` or just `s1`. The output will look
somewhat like this:

    $ s1
    ------------ Connections from: Universität s-Bahnhof, Dortmund  to: Dortmund hbf
         departure, arrival, delay, connection
        11:19,    11:26,    +0,    S
        11:39,    11:46,    +2,    S
        11:59,    12:06,    +3,    S
        12:19,    12:26,    +0,    S

Use s1 --help for more information


Module Usage
---------

Just import the module into your project and get a DBPageParser instance.

    from seins.PageParser import DBPageParser

    page = DBPageParser(departing_station, arrival_station, day=None, departure_time=None)
    #returns a list of tuples of the form (departure_time, arrival_time, delay, connection_type)
    connections = page.connections

You can specify an optional departure time and day. If not provided the current time and day will be used as defaults

The PageParser can produce some Exceptions depending on your input. Or if there are connection problems to the DB

    from seins.PageParser import DBPageParser, PageContentError
    from seins.HtmlFetcher import FetcherException

    try:
        page = DBPageParser(departing_station, arrival_station)

    except PageContentError as e:
        logger.error('Webpage returned an error message: ' + str(e))

    except FetcherException as e:
        logger.error('Fetcher could not get valid response from server: ' + str(e))

