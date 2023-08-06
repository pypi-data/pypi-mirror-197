from logging import getLogger, basicConfig, StreamHandler, DEBUG, INFO
from sys import stdout


class HandlerLogger(object):
    def __init__(self, logger_name):
        basicConfig(filename='acodis-handler-debug.log', filemode='a', format='%(name)s - %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level='DEBUG')

        basicConfig(filename='acodis-handler-info.log', filemode='a', format='%(name)s - %(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level='INFO')

        self.log = self.get_log(logger_name)

    def get_log(self, logger_name):
        log = getLogger(logger_name)
        log.addHandler(StreamHandler(stream=stdout))
        self.log = log
        return log
