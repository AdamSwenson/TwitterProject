"""
Created by adam on 6/25/18
"""
__author__ = 'adam'

import tornado.web
from tornado import gen
from tornado_sqlalchemy import SessionMixin

# Loggers and instrumentation
from Server.ServerTools.ServerExceptions import ShutdownCommanded


class IRequestHandler( tornado.web.RequestHandler, SessionMixin ):
    """Handles requests to save word mappings from user descriptions and tweets to the db """

    # def __init__( self, application, request, **kwargs ):
    #     super().__init__( application, request )

    @classmethod
    def increment_request_count( cls ):
        # increment the notification spinner
        cls.spinner.next()
        # add to the stored request count.
        cls._requestCount += 1

    @gen.coroutine
    def get( self ):
        """Flushes any remaining results in the queue to the dbs"""
        # print( "%s in queue; flushing now" % self.queue_length)
        # ql = self.queue_length
        yield from type( self ).q.save_queued()
        self.write( 'success' )


    @property
    def queue_length( self ):
        return len( type( self ).q.store )

    @classmethod
    def shutdown( cls ):
        """This handles the client side command to cease all
        server operations. That involves flushing the
        queue and writing to requisite log files"""
        # flush the queue (for this handler instance!)
        cls.q.save_queued()

        message = "Shutdown called. \n # requests: %s \n # queries: %s" % (cls._requestCount, cls._queryCount)
        print( message )
        cls.logger.log( message )
        # emit the command to shutdown the server
        raise ShutdownCommanded
        # (requests=cls._requestCount, queries=cls._queryCount)


if __name__ == '__main__':
    pass
