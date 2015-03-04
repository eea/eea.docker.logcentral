import logging
import time
from logging.handlers import SysLogHandler

if __name__ == '__main__':
    file_handler = SysLogHandler(address=('fluentd_1', 5140))
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
        print "We love docker"
        time.sleep(2)
