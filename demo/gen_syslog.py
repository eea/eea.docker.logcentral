#!/usr/bin/env python

import logging
import time
from logging.handlers import SysLogHandler

if __name__ == '__main__':
    file_handler = SysLogHandler(address=('10.201.1.151', 1514))
    formatter = logging.Formatter(
        '%(asctime)s lolcathost app1 : %(message)s', datefmt='%b %d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger = logging.getLogger('some_logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    while True:
        logger.debug('Debugging from app1')
        logger.info('Informing from app1')
        logger.critical('Criticalizing from app1')
        print "Sent syslog to fluentd"
        time.sleep(2)
