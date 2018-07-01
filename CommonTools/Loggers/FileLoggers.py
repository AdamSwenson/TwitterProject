"""
Created by adam on 3/26/18
"""

__author__ = 'adam'
import os

from logbook import FileHandler

from CommonTools.Loggers.ILogger import ILogger

BASE = os.getenv("HOME")
# todo restore environment
# from DataAnalysis.environment import *

# Logging
LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % BASE

DEFAULT_LOG_FILE_NAME = 'twitter_log.txt'
DEFAULT_LOG_FILE_PATH = "%s/%s" % (LOG_FOLDER_PATH, DEFAULT_LOG_FILE_NAME)


class FileWritingLogger(ILogger):

    def __init__(self,  **kwargs):
        """ kwargs may contain: name, log_path """
        self.name = 'Default'

        self._process_kwargs(kwargs)

        if hasattr(self, 'log_path') is False:
            self.log_path = DEFAULT_LOG_FILE_PATH

        print("%s Logging to: %s" % (self.name, self.log_path))

        log_handler = FileHandler(self.log_path)
        log_handler.push_application()

        super().__init__()

    def add_break( self ):
        self.log( "=====================================================" )



# class DBEventLogger(LogWriter):
#     """
#     Handles logging and printing information about database events
#     """
#
#     def __init__(self, CLIENT_SEND_LOG_FILE=DEFAULT_LOG_FILE_NAME):
#         self.log = ''
#         super().__init__()
#         self.CLIENT_SEND_LOG_FILE = CLIENT_SEND_LOG_FILE
#         # self.UPATH = os.getenv("HOME")
#         # self.CLIENT_SEND_LOG_FILE = '%s/Desktop/%s' % self.UPATH, CLIENT_SEND_LOG_FILE
#         # self.CLIENT_SEND_LOG_FILE = "application_search.log"
#         self.set_log_file(self.CLIENT_SEND_LOG_FILE)
