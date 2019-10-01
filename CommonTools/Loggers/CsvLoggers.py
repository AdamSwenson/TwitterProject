"""
Created by adam on 3/26/18
"""
import datetime

__author__ = 'adam'
import os

import csv

# from profiling.OptimizingTools import standard_timestamp

import environment as env

# query_log = '%s/QUERY_LOG.csv' % environment.LOG_FOLDER_PATH
# query_time_log = '%s/QUERY_TIME_LOG.csv' % environment.LOG_FOLDER_PATH
#
# request_log = '%s/request_log.csv' % environment.LOG_FOLDER_PATH
# request_time_log = '%s/request_time_log.csv' % environment.LOG_FOLDER_PATH

# DEFAULT_LOG_FILE_NAME = 'twitter_log.txt'
# DEFAULT_LOG_FILE_PATH = "%s/%s" % (environment.LOG_FOLDER_PATH, DEFAULT_LOG_FILE_NAME)


def log_query( seconds, logFile=env.QUERY_LOG ):
    """Writes the duration (in seconds) of the word_map_table_creation_query to the csv log file"""
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        writer.writerow( [ seconds ] )


def log_query_timestamp( logFile=env.QUERY_TIME_LOG ):
    """Writes the timestamp of when the word_map_table_creation_query happened to a csv log file"""
    pass
    # ts = standard_timestamp()
    # with open( logFile, 'a' ) as csvfile:
    #     writer = csv.writer( csvfile )
    #     writer.writerow( [ ts ] )


def log_request( seconds, logFile=env.REQUEST_LOG ):
    """Writes the duration (in seconds) of the request to the csv log file"""
    with open( logFile, 'a' ) as csvfile:
        writer = csv.writer( csvfile )
        writer.writerow( [ seconds ] )


def log_request_timestamp( logFile=env.REQUEST_TIME_LOG ):
    """Writes the timestamp of when the request happened to a csv log file"""
    pass
    # ts = standard_timestamp()
    # with open( logFile, 'a' ) as csvfile:
    #     writer = csv.writer( csvfile )
    #     writer.writerow( [ ts ] )
