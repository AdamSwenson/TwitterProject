"""
Created by adam on 3/27/18
"""
from Server.ServerTools.Mixins import ResponseStoreMixin
__author__ = 'adam'

from tornado import gen
import asyncio
from tornado.httpclient import AsyncHTTPClient
from tornado.log import gen_log
from tornado.simple_httpclient import SimpleAsyncHTTPClient

import environment as env

from Server.ServerTools.Routes import DB_INFO_ROUTE
from DataAnalysis.ProcessingTools.Mixins import ProcessIdHaver
from Server.ServerTools import Helpers

# instrumenting to determine if running async
from Profiling.OptimizingTools import timestamp_writer, timestamped_count_writer


class NoQueueTimeoutHTTPClient( SimpleAsyncHTTPClient ):
    def fetch_impl( self, request, callback ):
        key = object()

        self.queue.append( (key, request, callback) )
        self.waiting[ key ] = (request, callback, None)

        self._process_queue()

        if self.queue:
            gen_log.debug( "max_clients limit reached, request queued. %d active, %d queued requests." % (
                len( self.active ), len( self.queue )) )


AsyncHTTPClient.configure( NoQueueTimeoutHTTPClient )


class Client( ProcessIdHaver, ResponseStoreMixin ):

    @classmethod
    def initialize_client( cls ):
        """Create one client instance for all to share"""
        cls.http_client = AsyncHTTPClient()

    def __init__( self, url ):
        self.id_prefix = 'client.send'
        super().__init__()
        self.url = url
        self.sentCount = 0
        self.errorCount = 0
        self.successCount = 0

        if not hasattr( self, 'http_client' ):
            type( self ).initialize_client()

    @gen.coroutine
    def get_max_tweet_id( self ):
        url = "%s%s" % (env.DB_URL, DB_INFO_ROUTE)
        response = yield from self.http_client.fetch( url, method="GET")
        return response

    @gen.coroutine
    def send( self, result ):
        """Posts the result or  to the server, yields a future"""
        self.sentCount += 1
        payload = Helpers.encode_payload( result )
        try:
            response = yield from self.http_client.fetch( self.url, method="POST", body=payload )
            return response
        except Exception as e:
            print(e)

    def send_flush_command( self, future=None, repeat=100 ):
        """Instructs the server to flush the queue of whichever
        handler receives it to the db. The signal thus needs to be
        sent several times to make sure all the handlers receive it
        """
        print('requesting queue flush')
        for _ in range( 0, repeat ):
            self.http_client.fetch( self.url, method="GET" )

    async def async_send_flush_command( self, future=None, repeat=15 ):
        """Instructs the server to flush the queue of whichever
        handler receives it to the db. The signal thus needs to be
        sent several times to make sure all the handlers receive it
        """
        print('requesting queue flush')

        tasks = [ asyncio.ensure_future(self.http_client.fetch( self.url, method="GET" )) for _ in range( 0, repeat ) ]
        for future in asyncio.as_completed(tasks):
            data = await future

    def send_shutdown_command( self, future=None ):
        """Instructs the server to shut down"""
        self.http_client.fetch( self.url, method="DELETE" )
        if future is not None and not future.done():
            future.set_result('shutdown complete')

    def close( self ):
        self.http_client.close()

#
# # __slots__ = ['batch', 'batch_size', 'save', 'flush']
# class ServerQueueDropin( IQueueHandler, ProcessIdHaver ):
#     """
#     DEPRECATED
#     """
#
#     def __init__( self, batch_size=10 ):
#         self.id_prefix = 'sqdi.enque'
#         super().__init__()
#         self.batch_size = batch_size
#         self.enquedCount = 0
#         self.client = Client()
#         self.store = deque()
#         self.listeners = [ ]
#
#     @gen.coroutine
#     def enque( self, item ):
#         """
#         Push a result into the queue for saving to
#         the db server. Once the batch size has been reached,
#         it will be sent to the server
#         """
#         # write the timestamp to file
#         # we aren't using the decorator for fear
#         # it will mess up the async
#         timestamp_writer( environment.CLIENT_ENQUE_LOG_FILE )
#
#         self.enquedCount += 1
#         # print(self.pid, self.enquedCount)
#         self.store.appendleft( item )
#         if len( self.store ) >= self.batch_size:
#             # if we've reached the batch size, send batch to the server
#             b = [ self.store.pop() for i in range( 0, self.batch_size ) ]
#             self.client.send( b )
#             # return response.body
#         # return None
#
#     @property
#     def sentCount( self ):
#         return self.client.sentCount
#
#     @property
#     def successCount( self ):
#         return self.client.successCount
#
#     @property
#     def errorCount( self ):
#         return self.client.errorCount
#
#     def next( self ):
#         pass


if __name__ == "__main__":
    pass