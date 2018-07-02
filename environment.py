"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os
import sys
import configparser

############################ Locations  ############################
ROOT = os.getenv( "HOME" )
PROJ_BASE = os.path.abspath(os.path.dirname(__file__))

# Folders outside of the project foler
enclosing = os.path.abspath(os.path.dirname(PROJ_BASE))
print(PROJ_BASE)
print(enclosing)
CREDENTIALS_FOLDER_PATH = "%s/private_credentials" % enclosing
# Processed data files
DATA_FOLDER = "%s/private_data" % enclosing
DB_FOLDER = "%s/Desktop/TwitterDataAnalysisLogs/dbs" % ROOT
EXPERIMENTS_FOLDER = '%s/Experiments' % enclosing
LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % ROOT


######################## Configuration ############################
import argparse
parser = argparse.ArgumentParser()
# Config actually takes a value
parser.add_argument('--config',
                    help="The name of the config file. Omit config.ini",
                    default="testing")

# These are just flags
parser.add_argument('--analysis',
                    help="Load the configuration for data analysis",
                    default="data-analysis")
args = parser.parse_args()

configFile = '%s/configurations/%s.config.ini' % (PROJ_BASE, args.config)
print("Reading configuration from %s" % configFile)
config = configparser.ConfigParser()
config.read(configFile)

#### Global control variables
TEST = config['control'].getboolean('TEST')
ITEM_TYPE = config['control'].get('ITEM_TYPE')
LIMIT = config['control'].getint('LIMIT')
#### Logging
INTEGRITY_LOGGING = config['logging'].getboolean('INTEGRITY_LOGGING')
TIME_LOGGING = config['logging'].getboolean('TIME_LOGGING')
SLACK_NOTIFY = config['logging'].getboolean('SLACK_NOTIFY')
SLACK_HEARTBEAT_LIMIT = config['logging'].getint('SLACK_HEARTBEAT_LIMIT')
#### Queues
DB_QUEUE_SIZE = config['queues'].getint('DB_QUEUE_SIZE')
CLIENT_QUEUE_SIZE = config['queues'].getint('CLIENT_QUEUE_SIZE')
#### Database
CREDENTIAL_FILE = '%s/private_credentials/%s' % (CREDENTIALS_FOLDER_PATH, config['database'].get('CREDENTIALS_FILE'))
DB_PORT = config['database'].getint('DB_PORT')
DB_URL = "http://127.0.0.1:%s" % DB_PORT
WHICH_SERVER = config['control'].get('WHICH_SERVER')
ENGINE = config['database'].get('ENGINE')


############################## Locations of code ###############
# Project folder paths
ANALYSIS_PATH = "%s/DataAnalysis" % PROJ_BASE
COMMON_TOOLS_PATH = "%s/CommonTools" % PROJ_BASE
SERVER_PATH = "%s/TwitterDatabase" % PROJ_BASE
TEXT_TOOLS_PATH = "%s/TextProcessingTools" % PROJ_BASE
MINING_PATH = "%s/Mining" % PROJ_BASE
UNIT_TESTS_PATH = "%s/tests" % PROJ_BASE

# add everyone to path explicitly
sys.path.append( PROJ_BASE )
sys.path.append( ANALYSIS_PATH )
sys.path.append(COMMON_TOOLS_PATH)
sys.path.append(SERVER_PATH )
sys.path.append( TEXT_TOOLS_PATH )
sys.path.append( MINING_PATH )
sys.path.append(UNIT_TESTS_PATH)


#### Credentials
SLACK_CREDENTIAL_FILE = "%s/private_credentials/slack-credentials.xml" % CREDENTIALS_FOLDER_PATH
TWITTER_CREDENTIAL_FILE = "%s/private_credentials/twittercredentials2.xml" % CREDENTIALS_FOLDER_PATH

# MySql credentials
# CredentialLoader
#
# TEST_CREDENTIALS_FILE = '%s/tests/helpers/sql_local_testing_credentials.xml' % PROJ_BASE
#
# if TEST:
#     CREDENTIAL_FILE = TEST_CREDENTIALS_FILE
# else:
#     # CREDENTIAL_FILE = '%s/private_credentials/sql_local_credentials.xml' % BASE
#     CREDENTIAL_FILE = '%s/private_credentials/sql_miner_laptop_credentials.xml' % BASE


#### Data and experiments
MAPPING_PATH = "%s/DataAnalysis/mappings" % PROJ_BASE

#### DB files
# sqlite db files
# working folders
SQLITE_FILE = '%s/wordmapping.db' % LOG_FOLDER_PATH
SQLITE_FILE_CONNECTION_STRING = 'sqlite:////%s' % SQLITE_FILE
# the working file things get compiled into
MASTER_DB = '%s/master.db' % LOG_FOLDER_PATH

#### Processed data files
USER_DB_MASTER = '%s/user-databases/users-master.db' % DATA_FOLDER
USER_DB_NO_STOP = '%s/user-databases/users-no-stop.db' % DATA_FOLDER
TWEET_DB_MASTER = '%s/tweet-databases/tweets-master.db' % DATA_FOLDER
TWEET_DB_NO_STOP= '%s/tweet-databases/tweets-no-stop.db' % DATA_FOLDER
ID_MAP_DB = '%s/id-map.db' % DATA_FOLDER
MAX_DB_FILES = 10  # the maximum number of db files to create.

#### Logging
# Logging folder paths
PROFILING_LOG_FOLDER_PATH = "%s/profiling" % LOG_FOLDER_PATH
INTEGRITY_LOG_FOLDER_PATH = "%s/integrity" % LOG_FOLDER_PATH

## User flow logging (tracking progress of user)
PROCESSING_ENQUE_LOG_FILE = "%s/processing-enque.csv" % PROFILING_LOG_FOLDER_PATH
# records timestamp every time a list of results from a user are pushed into the
# client side queue from the processor
CLIENT_ENQUE_LOG_FILE = "%s/client-enque.csv" % INTEGRITY_LOG_FOLDER_PATH
CLIENT_SEND_LOG_FILE = "%s/client-send.csv" % INTEGRITY_LOG_FOLDER_PATH
SERVER_RECEIVE_LOG_FILE = "%s/server-receive.csv" % INTEGRITY_LOG_FOLDER_PATH
SERVER_SAVE_LOG_FILE = "%s/server-save.csv" % INTEGRITY_LOG_FOLDER_PATH

## Time logging
CLIENT_ENQUE_TIMESTAMP_LOG_FILE = "%s/client-enque.csv" % PROFILING_LOG_FOLDER_PATH
CLIENT_SEND_TIMESTAMP_LOG_FILE = "%s/client-send.csv" % PROFILING_LOG_FOLDER_PATH
SERVER_RECEIVE_TIMESTAMP_LOG_FILE = "%s/server-receive.csv" % PROFILING_LOG_FOLDER_PATH
SERVER_SAVE_TIMESTAMP_LOG_FILE = "%s/server-save.csv" % PROFILING_LOG_FOLDER_PATH
QUERY_LOG = '%s/QUERY_LOG.csv' % LOG_FOLDER_PATH
QUERY_TIME_LOG = '%s/QUERY_TIME_LOG.csv' % LOG_FOLDER_PATH

## Permanent logs
# semi-permanent log of how long it takes to run user processing
# this gets written to regardless of whether TIME_LOGGING is True
RUN_TIME_LOG = '%s/%s-processing-run-time-log.csv' % (LOG_FOLDER_PATH, ITEM_TYPE)

