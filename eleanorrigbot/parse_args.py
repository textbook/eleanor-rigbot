"""Functionality for parsing command line arguments."""
import argparse
import logging

__version__ = '0.3.1'

# https://www.flickr.com/places/info/12695850
LIVERPOOL = [-3.0087, 53.3261, -2.8180, 53.4751]


def parse_args(args):
    """Parse the command line arguments."""
    parser = _build_parser()
    return parser.parse_args(args)


def _build_parser():
    """Build the argument parser."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--verbose', '-v',
        action='store_const',
        const=logging.DEBUG,
        default=logging.INFO,
        dest='log_level',
        help='set the logging level to DEBUG for more output',
    )
    parser.add_argument(
        '--location', '-l',
        default=LIVERPOOL,
        help='specify a location to filter (defaults to Liverpool)',
        metavar=('SW_LON', 'SW_LAT', 'NE_LON', 'NE_LAT'),
        nargs=4,
        type=float,
    )
    parser.add_argument('--version', action='version', version=__version__)
    return parser
