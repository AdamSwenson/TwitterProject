"""
Saves tweets to the db.

Created by adam on 6/25/18
"""
__author__ = 'adam'

import asyncio

from progress.spinner import Spinner
from tornado import gen

import environment
from CommonTools.Profiling.OptimizingTools import timestamp_writer
# Loggers and instrumentation
from Loggers.FileLoggers import FileWritingLogger
from Server.Queues.OrmSaveQueue import OrmSaveQueue
from Server.RequestHandlers.HandlerParent import IRequestHandler
from Server.ServerTools import Helpers
from Server.ServerTools.ServerExceptions import DBExceptions
from TwitterDatabase.Models.TweetORM import TweetFactory, UserFactory
from Mining.SearchResultsProcessing.UserExtractionTools import extract_user_dict_from_tweet, add_audit_data_to_user


class TweetSaveHandler( IRequestHandler ):
    """Handles requests to save user datas to the db """

    # Queue results at class level so that any instance
    # can initiate a save for the queue. Also prevents losing
    # the queue if the batch size has not been reached when a handler
    # instance is done
    q = OrmSaveQueue()

    _requestCount = 0
    _queryCount = 0

    spinner = Spinner( 'Loading ' )

    # logger = FileWritingLogger( name='TweetSaveHandler' )

    def delete( self ):
        """closes all operations"""
        with self.make_session() as session:
            type( self ).shutdown(session)

    @gen.coroutine
    def get( self ):
        """Flushes any remaining results in the queue to the dbs"""
        print( "%s in queue; flushing now" % self.queue_length )
        with self.make_session() as session:
            yield from type( self ).q.save_queued( session )
        self.write( 'success' )

    @gen.coroutine
    def post( self ):
        """Handles the submision of a list of
        new tweets
        """
        if environment.TIME_LOGGING:
            timestamp_writer( environment.SERVER_RECEIVE_TIMESTAMP_LOG_FILE )

        type( self ).increment_request_count()

        try:
            # decode json
            payload = Helpers.decode_payload( self.request.body )

            # The payload is a list containing dictionaries
            tweets = [ TweetFactory( p ) for p in payload ]
            # now extract users from the tweet objects' other_data field
            users = [add_audit_data_to_user(UserFactory(extract_user_dict_from_tweet( tweet )), tweet.tweetID) for tweet in tweets]
            # add the users to the tweets list
            tweets += users

            with self.make_session() as session:
                yield from asyncio.ensure_future( type( self ).q.enque( tweets, session ) )
            self.write( "success" )

        except DBExceptions as e:
            print( 'db error: %s' % e.message )
            # self.logger.log_error('db error: %s' % e.message)

            # no need for the client to know
            self.write( "success" )


if __name__ == '__main__':
    pass
