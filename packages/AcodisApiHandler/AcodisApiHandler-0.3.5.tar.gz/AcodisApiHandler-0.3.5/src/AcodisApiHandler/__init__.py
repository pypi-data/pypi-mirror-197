from AcodisApiHandler.acodis_handler import *
from AcodisApiHandler.acodis_parser import *
from AcodisApiHandler.acodis_error import *
from AcodisApiHandler._acodis_logger import *

__all__ = ['AcodisApiHandler', 'extract_tags', 'AcodisError', 'AcodisApiError', 'AcodisAuthError', 'AcodisParsingError']

if __name__ == '__main__':
    print("version is: " + __version__)