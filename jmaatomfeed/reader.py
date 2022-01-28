#!/usr/bin/python3
#
# Atom Feed XML reader for JMA.
#
import os
import sys
import time
import logging
import logging.config
import argparse
from pathlib import PurePath

# include this application libraries.
from feedparser import JmaAtomFeedParser
from config import logging_dictconfig


class ProcOption(object):
    def __init__(self):
        self.verbose = False
        self.sleep_sec = 0
        self.urls = []


# define
"""
process exit code.
"""
APP_VER = '0.1.0'
APP_AUTHOR = 'Norimitsu Sugimoto <dictoss@live.jp>'

PROC_RET_SUCCESS = 0
PROC_RET_ERROR = 1
PROC_RET_USAGE = os.EX_USAGE

# global var.
g_opt = ProcOption()
g_logger = logging.getLogger(__name__)
g_debug = True


def load_feed(url):
    _parser = JmaAtomFeedParser()

    # download atom feed.
    _xmldata = None
    try:
        g_logger.info('download {}'.format(url))
        _xmldata = _parser.download(url)
    except Exception as e:
        g_logger.error('EXCEPT: %s', e)
        _xmldata = None

    _parser.loads(_xmldata)
    _list = _parser.get_entry_list()

    return _parser


def main():
    g_logger.info("Hello Atom Feed XML reader for JMA !")

    if 0 < g_opt.sleep_sec:
        g_logger.info('sleep {} seconds...'.format(g_opt.sleep_sec))
        time.sleep(g_opt.sleep_sec)
        g_logger.info('wake up !')
    else:
        g_logger.info('start program.')

    # load feed
    for u in g_opt.urls:
        g_logger.info('start feed. target: {}'.format(u))
        _feedparser = load_feed(u)

        _entry_list = _feedparser.get_entry_list()
        g_logger.debug('_entry_list = {}'.format(_entry_list))

        # parse jma xml each <entry> in feed.
        for e in _entry_list:
            # parse
            pass

    return PROC_RET_SUCCESS


if __name__ == '__main__':
    # parse args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url_or_path',
        nargs='*',
        help='feed xml url orpath')

    # option
    parser.add_argument(
        '-V', '--version', action='version',
        version='%(prog)s  Atom Feed XML reader for JMA {}'.format(APP_VER))
    parser.add_argument(
        '-s', '--sleep', type=float, default=0.0,
        help='sleep seconds before program start.')
    parser.add_argument(
        '-v', '--verbose', action="store_true",
        help='output verbose log.')

    args = parser.parse_args()

    # check and set paramter.
    if 0 < len(args.url_or_path):
        g_opt.urls = args.url_or_path
    else:
        parser.print_help()
        sys.exit()

    g_opt.sleep_sec = args.sleep
    g_opt.verbose = args.verbose

    if g_opt.verbose:
        logging_dictconfig['handlers']['console']['level'] = 'DEBUG'
        logging_dictconfig['root']['level'] = 'DEBUG'

    logging.config.dictConfig(logging_dictconfig)

    _ret = main()
    sys.exit(_ret)
