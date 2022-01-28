#!/usr/bin/python3
#
# Atom Feed XML reader for JMA config file.
#

import logging

logging_dictconfig = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(asctime)s,%(levelname)-8s,%(module)s,L%(lineno)s,%(message)s',
        },
        'simple': {
            'format': '%(asctime)s,%(levelname)-8s,%(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'stream': 'ext://sys.stderr',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console'],
    },
    'disable_existing_loggers': False,
}
