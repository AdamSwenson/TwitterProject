"""
Created by adam on 6/25/18
"""
import sqlalchemy

__author__ = 'adam'

from collections.__init__ import deque
from progress.spinner import MoonSpinner
from tornado import gen, locks
from CommonTools.Loggers.FileLoggers import FileWritingLogger
from CommonTools.FileTools.CsvFileTools import write_csv
from Profiling.OptimizingTools import standard_timestamp
from TwitterDatabase.Models.TweetORM import Tweet, User
from TwitterDatabase.Repositories.NewOrmRepositories import update_tweet_if_changed
lock = locks.Lock()

import environment

logpath = "%s/mining/twitter-utf-fuckup.txt" % environment.LOG_FOLDER_PATH
csvlog = "%s/mining/twitter-save-data.csv" % environment.LOG_FOLDER_PATH
Logger = FileWritingLogger( log_path=logpath, name='OrmSaveQueue' )


class OrmSaveQueue:
    spinner = MoonSpinner()

    def __init__( self, batch_size=environment.DB_QUEUE_SIZE ):
        # number of times save is called
        self._queryCount = 0
        # number of items actually saved
        self._saveCount = 0
        # number of items attempted to save
        self._saveAttemptCount = 0
        # number invalid tweets
        self._invalidCount = 0
        # number of updated tweets
        self._updatedCount = 0
        # number of users whose data has been updated from tweets
        self._usersUpdatedCount = 0

        self.batch_size = batch_size
        self.store = deque()

    def increment_query_count( self ):
        # increment the notification spinner
        type( self ).spinner.next()
        # add to the stored request count.
        self._queryCount += 1

    @gen.coroutine
    def enque( self, modelList: list, session=None ):
        """
        Push a list of users into the queue for saving to
        the db. Once the batch size has been reached,
        it will be saved.
        The session is an instance of a sqlalchemy session
        :param session:
        :type modelList: list
        """
        with (yield lock.acquire()):
            # Push the model objects into the queue
            # we need to use the lock so that no other
            # instance gets in the way
            [ self.store.append( r ) for r in modelList ]

        # if we've reached the batch size, we save them to the db
        # needs to be greater in case hit limit in middle of list
        if len( self.store ) >= self.batch_size:
            yield from self.save_queued( session )

    async def save_queued( self, session ):
        """Flushes the orm objects in the queue to the database"""
        self.increment_query_count()

        async with lock:
            if len( self.store ) == 0: return True

            b = [ self.store.pop() for _ in range( 0, len( self.store ) ) ]

            for o in b:
                self._saveAttemptCount += 1
                try:
                    session.add( o )
                    session.commit()
                    self._saveCount += 1
                except sqlalchemy.exc.IntegrityError as e:
                    # print('integrity error %s' % e)
                    # The obj already exists, so we can try updating it
                    # first, we get rid of the attempted save
                    session.rollback()
                    # now try updating
                    self.update_handler(o, session)
                except sqlalchemy.exc.DatabaseError as e:
                    # print('db error %s' % e)
                    self._invalidCount += 1
                    session.rollback()
                except sqlalchemy.orm.exc.FlushError:
                    self._invalidCount += 1
                    session.rollback()

            self.record_stats()

    def record_stats( self ):
        save_rate = self._saveCount / self._saveAttemptCount

        r = [ standard_timestamp(), self._saveAttemptCount, self._saveCount, save_rate, self._invalidCount, self._updatedCount, self._usersUpdatedCount ]
        write_csv( csvlog, r )

        Logger.log( " ------------ ---------------- ------------ " )
        Logger.log( "Save attempt count %s" % self._saveAttemptCount )
        Logger.log( "Save success count %s" % self._saveCount )
        Logger.log( "Save rate          %s" % save_rate )
        Logger.log( "Invalid tweets     %s" % self._invalidCount )
        Logger.log( "Updated tweets     %s" % self._updatedCount )
        Logger.log( "Updated users     %s" % self._usersUpdatedCount )
        self.reset_counts()

    def reset_counts( self ):
        self._saveAttemptCount = 0
        self._saveCount = 0
        self._invalidCount = 0
        self._updatedCount = 0
        self._usersUpdatedCount = 0

    def update_handler( self, ormObject , session):
        """This is called when there has been an integrity error,
        which indicates that the object already exists. It determines
        what sort of object we're dealing with and dispatches the appropriate
        task to update it
        """
        # Determine what we're dealing with
        if isinstance(ormObject, Tweet):
            if update_tweet_if_changed(ormObject, session):
                self._updatedCount += 1
                # print("updated %s" % self._updatedCount)

        elif isinstance(ormObject, User):
            # This is just what the handler for tweets does.
            # Was more ambitious under TWIT-38, but not sure need
            # all the extra apparatus
            session.merge(ormObject)
            session.commit()
            self._usersUpdatedCount += 1


        # except Exception as e:

        # print( "error  %s " % e )
        # raise e

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
