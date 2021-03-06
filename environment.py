"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os
import sys
import configparser

############################ Locations  ############################
ROOT = os.getenv( "HOME" )

# The folder containing environment.py
PROJ_BASE = os.path.abspath(os.path.dirname(__file__))

# Folders outside of the project foler. This will usually
# be the credentials folder, logs and other things which should
# not be in version control
enclosing = os.path.abspath(os.path.dirname(PROJ_BASE))

# All login credentials are defined in files here.
# THIS FOLDER MUST NOT BE COMMITTED TO VERSION CONTROL!
CREDENTIALS_FOLDER_PATH = "%s/private_credentials" % enclosing

# Processed data files
DATA_FOLDER = "%s/private_data" % enclosing
DB_FOLDER = "%s/Desktop/TwitterDataAnalysisLogs/dbs" % ROOT

# Where parameters for experiments are defined
EXPERIMENTS_FOLDER = '%s/Experiments' % enclosing

# Where to put log files
# LOG_FOLDER_PATH = "%s/Desktop/TwitterDataAnalysisLogs" % ROOT


######################## Configuration ############################
""" 
On command line:
    python Folder/Executables/file.py --config=data-analysis

NB, for ipython, do this to inject config value at top of notebook
    import sys
    sys.argv = ['data-analysis']
    import environment
"""

print(sys.argv)
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
# These are just flags
parser.add_argument('--testing',
                    help="Load the configuration for data analysis",
                    default="testing")

parser.add_argument('--live',
                    help="Load the configuration for connecting to the csun ent db",
                    default="live-db")
# These are just flags

args = parser.parse_args()

configFile = '%s/configurations/%s.config.ini' % (PROJ_BASE, args.config)
print("Reading configuration from %s" % configFile)
config = configparser.ConfigParser()
config.read(configFile)

#### Global control variables
TEST = config['control'].getboolean('TEST')
ITEM_TYPE = config['control'].get('ITEM_TYPE')
LIMIT = config['control'].get('LIMIT')
LIMIT = None if LIMIT == 'None' else int(LIMIT)

#### Logging
LOG_FOLDER_PATH = config['logging'].get('LOG_FOLDER_PATH')
LOG_FOLDER_PATH = LOG_FOLDER_PATH.format(ROOT)
# print(LOG_FOLDER_PATH)
INTEGRITY_LOGGING = config['logging'].getboolean('INTEGRITY_LOGGING')
TIME_LOGGING = config['logging'].getboolean('TIME_LOGGING')
SLACK_NOTIFY = config['logging'].getboolean('SLACK_NOTIFY')
SLACK_HEARTBEAT_LIMIT = config['logging'].getint('SLACK_HEARTBEAT_LIMIT')
# Log files
DEFAULT_LOG_FILE_NAME = 'twitter_log.txt'
DEFAULT_LOG_FILE_PATH = "%s/%s" % (LOG_FOLDER_PATH, DEFAULT_LOG_FILE_NAME)

QUERY_LOG = '%s/QUERY_LOG.csv' % LOG_FOLDER_PATH
QUERY_TIME_LOG = '%s/QUERY_TIME_LOG.csv' % LOG_FOLDER_PATH

REQUEST_LOG = '%s/request_log.csv' % LOG_FOLDER_PATH
REQUEST_TIME_LOG = '%s/request_time_log.csv' % LOG_FOLDER_PATH

SEARCH_LOG = '{}/twitter_miner_log.txt'.format( LOG_FOLDER_PATH )


#### Queues
DB_QUEUE_SIZE = config['queues'].getint('DB_QUEUE_SIZE')
CLIENT_QUEUE_SIZE = config['queues'].getint('CLIENT_QUEUE_SIZE')

#### Database
CREDENTIAL_FILE = '%s/%s' % (CREDENTIALS_FOLDER_PATH, config['database'].get('CREDENTIALS_FILE'))
DB_PORT = config['database'].getint('DB_PORT')
DB_URL = "http://127.0.0.1:%s" % DB_PORT
WHICH_SERVER = config['database'].get('WHICH_SERVER')
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
SLACK_CREDENTIAL_FILE = "%s/slack-credentials.xml" % CREDENTIALS_FOLDER_PATH
TWITTER_CREDENTIAL_FILE = "%s/twittercredentials2.xml" % CREDENTIALS_FOLDER_PATH

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

