# -*- coding: utf-8 -*-
__author__ = 'mackaiver'

#Lets start with a simple commandline tool
import argparse
import os
from seins.PageParser import DBPageParser


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
    #do some pretty printing
    print('------------ Connections from:' + departure + '  to: ' + arrival)
    for c in page.connections:
        print(c)
    if output_path:
        with open(output_path, 'wt') as file:
            file.write(page.html)
            logger.info("Output written to " + output_path)