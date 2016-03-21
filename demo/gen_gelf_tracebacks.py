#!/usr/bin/env python

"""
How to use graypy to log _FULL_
exceptions to graylog2 by bypassing syslog
"""

import graypy
import logging
import random
import time

if __name__ == '__main__':
    gelf_handler = graypy.GELFHandler('localhost')
    root_logger = logging.getLogger()

    # Add the GELF handler to the root loggers so all new loggers will
    # automatically use it when logging exceptions
    root_logger.addHandler(gelf_handler)
    
    logger = []
    
    for n in range(2000):
        log = logging.getLogger('logger_%s' % n)
        log.setLevel(logging.DEBUG)
        logger.append(log)

    my_dict = {}

    while True:
        key = random.randint(10, 2000)
        try:
            print my_dict[key]
        except KeyError as e:
            i = 0
            for log in logger:
                if i % 2 == 0:
                   log.debug('Had this key error %d', key, exc_info=1)
                else:
                   log.info('Handlers are inherited from the root logger')
                i =  i + 1
                print "logged directly to graylog2"
        time.sleep(2)
