import logging
import time
from logging.handlers import SysLogHandler

if __name__ == '__main__':
    file_handler = SysLogHandler(address=('fluentd_1', 5140))
    formatter = logging.Formatter(
        '%(asctime)s coolcathost app2 : %(message)s', datefmt='%b %d %H:%M:%S')
    file_handler.setFormatter(formatter)
    logger = logging.getLogger('some_logger')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    while True:
        logger.debug('Debugging from app2')
        logger.critical('constant failing is constant')
        print 'we love logging'
        time.sleep(2)
