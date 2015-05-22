#!/usr/bin/env python

"""
How to use graypy to log _FULL_
exceptions to graylog2 by bypassing syslog
"""

from graypy import rabbitmq
import logging
import random
import time

if __name__ == '__main__':
    # Use this URI base and replace the host with the actual host you want
    # to configure
    URI_BASE = 'amqp://guest:guest@{host}:5672/%2F'
    gelf_handler = rabbitmq.GELFRabbitHandler(URI_BASE.format(host='localhost'))
    root_logger = logging.getLogger()

    # Add the GELF handler to the root loggers so all new loggers will
    # automatically use it when logging exceptions
    root_logger.addHandler(gelf_handler)

    logger1 = logging.getLogger('logger_1')
    logger2 = logging.getLogger('logger_2')
    logger1.setLevel(logging.DEBUG)
    logger2.setLevel(logging.DEBUG)

    my_dict = {}

    while True:
        key = random.randint(10, 2000)
        try:
            print my_dict[key]
        except KeyError as e:
            logger1.debug('Had this key error %d', key, exc_info=1)
            logger2.info('Handlers are inherited from the root logger')
            print "logged directly to graylog2"
        time.sleep(2)
