"""
Created by adam on 6/25/18
"""
__author__ = 'adam'

import asyncio

from collections.__init__ import deque
from progress.spinner import MoonSpinner
from tornado import gen, locks

from Profiling.OptimizingTools import timestamp_writer

lock = locks.Lock()
from tornado_sqlalchemy import SessionMixin, as_future

import environment


class OrmSaveQueue:
    spinner = MoonSpinner()

    def __init__( self, batch_size=environment.DB_QUEUE_SIZE ):
        self._queryCount = 0
        self.batch_size = batch_size
        self.store = deque()

    def increment_query_count( self ):
        # increment the notification spinner
        type( self ).spinner.next()
        # add to the stored request count.
        self._queryCount += 1

    @gen.coroutine
    def enque( self, userList: list, session=None ):  # : asyncio.Future ):
        """
        Push a list of users into the queue for saving to
        the db. Once the batch size has been reached,
        it will be saved.
        The session is an instance of a sqlalchemy session
        :param session:
        :type userList: list
        """
        # Handle logging
        # if environment.TIME_LOGGING:
        #     timestamp_writer( environment.CLIENT_ENQUE_TIMESTAMP_LOG_FILE )
        # if environment.INTEGRITY_LOGGING:
        #     [timestamped_count_writer(environment.CLIENT_ENQUE_LOG_FILE, r.id, 'userid') for r in resultList]
        with (yield lock.acquire()):
            # Push the user objects into the queue
            # we need to use the lock so that no other
            # instance gets in the way
            # async with lock:
            [ self.store.appendleft( r ) for r in userList ]
            print( len( self.store ), self.batch_size )

        # if we've reached the batch size, we save them to the db
        # needs to be greater in case hit limit in middle of list
        if len( self.store ) >= self.batch_size:
            yield from self.save_queued( session )

    async def save_queued( self, session ):
        """Flushes the user objects in the queue to the database"""
        self.increment_query_count()

        # if environment.TIME_LOGGING:
        #     timestamp_writer( environment.SERVER_SAVE_TIMESTAMP_LOG_FILE )

        async with lock:
            try:
                b = [ self.store.pop() for _ in range( 0, self.batch_size ) ]
                # with self.make_session() as session:
                session.add_all( b )
                print( len( session.new ) )
                session.commit()
            except Exception as e:
                print( "error  %s " % e )
                raise e

    #
    # async def handle_send( self, future: asyncio.Future ):
    #     """Passes the current queue items to the client
    #     and clears queue.
    #     This bastard not being async wasted a week of my life
    #     :type future: asyncio.Future
    #     """
    #     b = [ self.store.pop() for _ in range( 0, self.batch_size ) ]
    #
    #     await self.client.send( b )
    #
    #     # mark future as done
    #     # (we aren't waiting for the result, just the sending)
    #     future.set_result(True)
    #     return future
    # #
    # async def flush_queue( self, future ):
    #     """Sends everything in queue to server"""
    #     b = [ self.store.pop() for _ in range( 0, len(self.store )) ]
    #
    #     await self.client.send( b )
    #
    #     # mark future as done
    #     # (we aren't waiting for the result, just the sending)
    #     future.set_result(True)
    #     return future
    #

    # @gen.coroutine
    # def enqueue( self, user ):
    #     """
    #     Asynchronously push a result onto the queue to be saved when
    #     an adequate number is reached
    #     :param user:
    #     :return:
    #     """
    #
    #     with self.make_session() as session:
    #         # We've now filled the user object with data from the result
    #         # so we add it to the session but do not yet flush it
    #         session.add( user )
    #         print(session.new)
    #     # self.session.add( user )
    #
    #     # nb can't use native future object
    #     #     yield as_future(type( self ).q.save_queued())
    #
    #     # print(self.session.new)
    #     # with (yield lock.acquire()):
    #     #     if len(self.session.new) > self.batch_size:
    #     #         yield from self.save_queued()

    # async def save_queued( self ):
    #     self.increment_query_count()
    #     async with lock:
    #         try:
    #             if environment.TIME_LOGGING:
    #                 timestamp_writer( environment.SERVER_SAVE_TIMESTAMP_LOG_FILE )
    #             self.session.commit()
    #
    #         except Exception as e:
    #             print( "error for file %s : %s" % (self.file_path, e) )
    #


if __name__ == '__main__':
    pass
