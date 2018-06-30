"""
Automatically downloads tweets for the provided terms

NB, this used to be called 'Automine4.py'
"""
from CouchDB.CouchDBDAOs import CouchDAO
# from deprecated import TwitterSQLService
from CommonTools.Loggers.SearchLoggers import SearchLogger

from Mining.DatabaseTools.MySQLTools import *
from Redis.RedisToolsAlso import *
from Mining.SearchResultsProcessing.TweetResults import *
from Mining.Miner.TwitterSearchTools import *
from Mining.Miner.ObserverAndSubscribers import MySqlSaver, CouchSaver, RedisSaver, SearchObserver
from Credentialing import SqlCredentials

# Better way to find home
import os
UPATH = os.getenv("HOME")
BASE = '%s/Dropbox/TwitterProject' % UPATH


DB_NAME = 'compiled'
limit = 10000
LOGFILE = '%s/Desktop/twitter_miner_log.txt' % UPATH
# LOGFILE = '/Users/adam/Desktop/twitter_miner_log.txt'
REST = 800  # Interval to rest between runs

SQL_CREDENTIALS = "%s/private_credentials/sql_local_credentials.xml" % BASE
TWITTER_CREDENTIALS = "%s/private_credentials/twittercredentials.xml" % BASE

#search_terms = ['Migraine', 'RSD']

search_terms = ['Spoonie',
                 'CRPS',
                 'Migraine',
                 'RSD',
                 'Fibro',
                 'Fibromyalgia',
                 'Vulvodynia',
                 'ChronicPain',
                 'pain',
                 'endometriosis',
                 'neuropathy',
                 'arthritis',
                 'neuralgia']

# Utility classes
Logger = SearchLogger()
Logger.set_log_file(LOGFILE)
TagHelpers = TagHelpers()

# Initialize couchdb handler classes
couch_dao = CouchDAO()
couch_dao.connect(DB_NAME)
couch_service = CouchService()
couch_service.set_dataservice(couch_dao)
CouchSaver = CouchSaver()
CouchSaver.set_dao(couch_service)

# Initialize redis handler classes
RedisService = RedisService()
RedisSaver = RedisSaver()
RedisSaver.set_dao(RedisService)

# Initialize mysql handler classes
credentials = SqlCredentials.Credentials()
credentials.load_credentials(SQL_CREDENTIALS)
mysql_dao = TwitterSQLService.SQLService( credentials )
# Initialize services for mysql
TweetService = TweetService()
TweetService.set_helper(TagHelpers)
TweetService.set_dao(mysql_dao)

HashtagService = HashtagService()
HashtagService.set_helper(TagHelpers)
HashtagService.set_dao(mysql_dao)

UserService = UserService()
UserService.set_dao(mysql_dao)

MySqlSaver = MySqlSaver()
MySqlSaver.set_services(HashtagService, TweetService, UserService)

# Initialize observer and attach saver objects to it
SaverService = SearchObserver()
SaverService.subscribe_db_saver(RedisSaver)
SaverService.subscribe_db_saver(CouchSaver)
SaverService.subscribe_db_saver(MySqlSaver)

# add some sort of check to make sure everything is ready before starting search

# Initialize classes which perform the searching
Searcher = Search()
Searcher.set_couch_service(CouchService)
Searcher.set_redis_service(RedisService)
Searcher.set_logger(Logger)
Searcher.attach_observer(SaverService)


def getNewerTweets():
    """
    Call this to get the most recent tweets for the search list
    """
    recent = True
    Searcher.set_twitter_connection( TWITTER_CREDENTIALS)
    Searcher.run(search_terms, limit, recent, REST)


def getOlderTweets():
    """
    Call this to get tweets older than those already stored
    """
    recent = False
    Searcher.set_twitter_connection( TWITTER_CREDENTIALS)
    Searcher.run(search_terms, limit, recent, REST)

getNewerTweets()
