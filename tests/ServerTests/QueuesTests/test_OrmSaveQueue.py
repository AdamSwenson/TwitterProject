import asyncio

import aiounittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from Server.Queues.OrmSaveQueue import OrmSaveQueue
from tests.helpers.Factories import UserFactory

# import tornado
# from tornado.testing import gen_test
# from tornado.testing import AsyncHTTPTestCase, AsyncTestCase
#
# from TwitterDatabase.DatabaseAccessObjects.EngineMakers import create_sqlite_engine
#
# class S:
#     def __init__( self ):
#         pass
#
#     def get( self, thing ):
#         return make_session_factory( 'sqlite://' )
#
# class A:
#     def __init__( self ):
#         self.settings = S()


from tests.helpers import settings
from tests.helpers import table_creation_queries as queries

session = settings.Session()
session.execute(queries.make_users_table)
session.commit()


class OrmSaveQueueTest( aiounittest.AsyncTestCase ):

    def setUp( self ):
        self.session = session
        self.numUsers = 30
        # self.incomingPayload = [encode_payload(u) for u in self.users]
        self.obj = OrmSaveQueue( self.numUsers )
        self.users = [ UserFactory() for _ in range( 0, self.numUsers ) ]

    # create a Session

    def tearDown(self):
        self.session.rollback()
        settings.Session.remove()

    # def test_enque_are_coroutine_functions( self ):
    #     self.assertEqual(asyncio.iscoroutinefunction(self.obj.enque), True, "enque is coroutine function")

    def test_save_is_coroutine_function( self ):
        self.assertEqual( asyncio.iscoroutinefunction( self.obj.save_queued ), True, "save is coroutine function" )

    async def test_enque_sub_batch_size( self ):
        expect = self.numUsers - 4
        await asyncio.ensure_future( self.obj.enque( self.users[ : expect ] ) )
        self.assertEqual( len( self.obj.store ), expect, "not flushed to db" )
        # self.assertEqual(True, False)

    async def test_enque_flushes_at_batch_size( self ):
        await asyncio.ensure_future( self.obj.enque( self.users, self.session ) )
        self.assertEqual( len( self.obj.store ), 0, "flushed to db" )

    async def test_save_queued( self ):
        self.obj.store = self.users
        await asyncio.ensure_future( self.obj.save_queued( self.session ) )
        self.assertEqual( len( self.obj.store ), 0 )
