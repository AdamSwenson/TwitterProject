"""
Created by adam on 6/25/18
"""
__author__ = 'adam'

import sqlite3

from collections.__init__ import deque
from progress.spinner import MoonSpinner
from tornado import gen, locks

import environment
from Profiling.OptimizingTools import timestamp_writer

lock = locks.Lock()


class WordMapSaveQueue( object ):
    spinner = MoonSpinner()

    def __init__( self, batch_size=environment.DB_QUEUE_SIZE, file_path=environment.MASTER_DB ):
        self._queryCount = 0
        self.batch_size = batch_size
        self.store = deque()
        self.file_path = file_path
        self.user_query = """
        INSERT INTO word_map 
          (word, sentence_index, word_index, user_id) 
        VALUES (?, ?, ?, ?)
        """
        self.tweet_query = """
        INSERT INTO word_map 
          (word, sentence_index, word_index, tweet_id) 
        VALUES (?, ?, ?, ?)
        """
        # use the environent to set which word_map_table_creation_query we use
        self.query = self.tweet_query if environment.ITEM_TYPE == 'tweet' else self.user_query

    def increment_query_count( self ):
        # increment the notification spinner
        type( self ).spinner.next()
        # add to the stored request count.
        self._queryCount += 1

    @gen.coroutine
    def enqueue( self, result ):
        rt = (result.text, result.sentence_index, result.word_index, result.id)
        with (yield lock.acquire()):
            self.store.appendleft( rt )
        if len( self.store ) > self.batch_size:
            yield from self.save_queued()

    async def save_queued( self ):
        """Saves all the items in the queue to the db
        To help with isolation levels From https://www.sqlite.org/lang_transaction.html
        Transactions can be deferred, immediate, or exclusive. The
        default transaction behavior is deferred. Deferred means that no locks are acquired on the database until the
        database is first accessed. Thus with a deferred transaction, the BEGIN statement itself does nothing to the
        filesystem. Locks are not acquired until the first read or write operation. The first read operation against
        a database creates a SHARED lock and the first write operation creates a RESERVED lock. Because the
        acquisition of locks is deferred until they are needed, it is possible that another thread or process could
        create a separate transaction and write to the database after the BEGIN on the current thread has executed.
        If the transaction is immediate, then RESERVED locks are acquired on all databases as soon as the BEGIN
        command is executed, without waiting for the database to be used. After a BEGIN IMMEDIATE, no other database
        connection will be able to write to the database or do a BEGIN IMMEDIATE or BEGIN EXCLUSIVE. Other processes
        can continue to read from the database, however. An exclusive transaction causes EXCLUSIVE locks to be
        acquired on all databases. After a BEGIN EXCLUSIVE, no other database connection except for read_uncommitted
        connections will be able to read the database and no other connection without exception will be able
        to write  the database until the transaction is complete.
        """
        self.increment_query_count()
        async with lock:
            try:
                if environment.TIME_LOGGING:
                    timestamp_writer( environment.SERVER_SAVE_TIMESTAMP_LOG_FILE )

                # create a new connection so not sharing across threads (which is not allowed)
                conn = sqlite3.connect( self.file_path, isolation_level="EXCLUSIVE" )
                # wrap in a transaction so that other processess can play nice
                with conn:
                    rs = [ self.store.pop() for i in range( 0, len( self.store ) ) ]

                    conn.executemany( self.query, rs )

            except Exception as e:
                print( "error for file %s : %s" % (self.file_path, e) )
