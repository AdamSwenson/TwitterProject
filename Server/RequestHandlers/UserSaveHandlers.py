"""
Saves users to the db.

Created by adam on 6/25/18
"""
__author__ = 'adam'

import asyncio


from progress.spinner import Spinner
from tornado import gen

import environment
from CommonTools.Profiling.OptimizingTools import timestamp_writer, timestamped_count_writer
# Loggers and instrumentation
from Loggers.FileLoggers import FileWritingLogger
from Server.ServerTools import Helpers
from Server.ServerTools.ServerExceptions import DBExceptions
from Queues.OrmSaveQueue import OrmSaveQueue
from Server.RequestHandlers.HandlerParent import IRequestHandler
from TwitterDatabase.Models.TweetORM import UserFactory


class UserSaveHandler( IRequestHandler ):
    """Handles requests to save user datas to the db """

    # Queue results at class level so that any instance
    # can initiate a save for the queue. Also prevents losing
    # the queue if the batch size has not been reached when a handler
    # instance is done
    q = OrmSaveQueue()

    _requestCount = 0
    _queryCount = 0

    spinner = Spinner( 'Loading ' )

    logger = FileWritingLogger( name='UserSaveHandler' )

    def delete( self ):
        """closes all operations"""
        type( self ).shutdown()

    @gen.coroutine
    def get( self ):
        """Flushes any remaining results in the queue to the dbs"""
        # print( "%s in queue; flushing now" % self.queue_length)
        # ql = self.queue_length
        yield from type( self ).q.save_queued()
        self.write( 'success' )


    @gen.coroutine
    def post( self ):
        """Handles the submision of a list of
        new user-word records.
        """
        if environment.TIME_LOGGING:
            timestamp_writer( environment.SERVER_RECEIVE_TIMESTAMP_LOG_FILE )

        type( self ).increment_request_count()

        try:
            # decode json
            payload = Helpers.decode_payload( self.request.body )
            # The payload is a list containing dictionaries
            users = [UserFactory(p) for p in payload]
            #     if environment.INTEGRITY_LOGGING:
            #         timestamped_count_writer( environment.SERVER_RECEIVE_LOG_FILE, user.userID, 'userid' )

            yield from asyncio.ensure_future(type( self ).q.enque( users, self.session ))
            self.write( "success" )

        except DBExceptions as e:
            # self.logger.log_error('db error: %s' % e.message)
            self.write( "error" )

