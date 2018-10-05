#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
[options.entry_points] section in setup.cfg:

    console_scripts =
         fibonacci = mlneth_backend.skeleton:run

Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
Besides console scripts, the header (i.e. until _logger...) of this file can
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging
from db import DataBase
from images import *
from events_loader import get_events_list
# from sets import Set

from mlneth_backend import __version__

__author__ = "porobov"
__copyright__ = "porobov"
__license__ = "mit"

_logger = logging.getLogger(__name__)






def fib(n):
    """Fibonacci example function

    Args:
      n (int): integer

    Returns:
      int: n-th Fibonacci number
    """
    assert n > 0
    a, b = 1, 1
    for i in range(n-1):
        a, b = b, a+b
    return a


def parse_args(args):
    """Parse command line parameters

    Args:
      args ([str]): command line parameters as list of strings

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    parser = argparse.ArgumentParser(
        description="Just a Fibonnaci demonstration")
    parser.add_argument(
        '--version',
        action='version',
        version='mlneth-backend {ver}'.format(ver=__version__))
    parser.add_argument(
        dest="n",
        help="n-th Fibonacci number",
        type=int,
        metavar="INT")
    parser.add_argument(
        '-v',
        '--verbose',
        dest="loglevel",
        help="set loglevel to INFO",
        action='store_const',
        const=logging.INFO)
    parser.add_argument(
        '-vv',
        '--very-verbose',
        dest="loglevel",
        help="set loglevel to DEBUG",
        action='store_const',
        const=logging.DEBUG)
    return parser.parse_args(args)


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")

def calc_visible_banners(banner_events):
    # logging.debug("BigPicture. Preparing banners...")
    occupied = set()
    new_banners = []
    # retrieve banners in reverse order

    for banner in banner_events:
        new_coords = set()
        enough_space = True
        for iy in range(banner.y1, banner.y2, 10):
            for ix in range(banner.x1, banner.x2, 10):
                new_coords.add((ix, iy))
                if (ix, iy) in occupied:  # TODO check (ix >= size) or (iy >= size)):
                    enough_space = False
        if enough_space:
            new_banners.append(banner)
            occupied = occupied.union(new_coords)
        if len(occupied) >= 10000:
            # logging.info("all 10 000 blocks are occupied")
            break
    # logging.debug("BigPicture. Banners count: " + str(len(new_banners)) + ". " +
    #              "Blocks occupied: " + str(len(occupied)))
    return new_banners

def main(args):
    """Main entry point allowing external calls
    Args:
      args ([str]): command line parameter list
    """

    # args = parse_args(args)
    # setup_logging(args.loglevel)
    # _logger.debug("Starting crazy calculations...")

    # DOWNLOAD EVENTS
    # get last block processed
    # load events for new banners (from block)
    # validate banners data
    # write banners to DB
    # update last block processed
    
    data_base = DataBase()
    # data_base.write_events(get_events_list('NewImage', 2800200, 5864031))

    # DOWNLOAD IMAGES
    # find banners with no local image
    new_banners = data_base.get_new_banners()
    for banner in new_banners:
        # abs to deal with a bug in old smart contract
        width = abs(banner.x2 - banner.x1)
        height = abs(banner.y2 - banner.y1)
        # download, validate and format images
        local_path, error = download_image(banner.id, banner.src, width, height)
        data_base.update_local_image(banner, local_path, error)
        
    # CREATE BIG PICTURE AND HTML
    all_banners = data_base.get_all_banners()
    visible_banners = calc_visible_banners(all_banners)
    new_big_picture_path = new_big_picture(visible_banners)
    print(new_big_picture_path)
    
    # if new banner id build bigpicture
    # if new banner id build html

    _logger.info("Script ends here")


def run():
    """Entry point for console_scripts
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    run()
