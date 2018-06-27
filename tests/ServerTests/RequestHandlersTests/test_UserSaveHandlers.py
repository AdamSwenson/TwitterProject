import unittest

import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado_sqlalchemy import make_session_factory

from Server.RequestHandlers.UserSaveHandlers import UserSaveHandler
from tests.helpers.TwitterSearchResultFactories import UserSearchResultFactory


# from aiounittest import futurized, AsyncTestCase



def serializeUserResult( result ):
    return { k: getattr( result, k ) for k in result.__dict__ }


class UserSaveHandlersTests( AsyncHTTPTestCase ):
    def get_app( self ):
        factory = make_session_factory( 'sqlite://' )
        return tornado.web.Application( [ (r'/', UserSaveHandler) ], session_factory=factory )

    def test_post( self ):
        self.numUsers = 30
        self.users = [ serializeUserResult( UserSearchResultFactory() ) for _ in range( 0, self.numUsers ) ]
        self.incomingPayload = tornado.escape.json_encode( self.users )  # for u in self.users ]

        # call
        response = self.fetch( '/', method="POST", body=self.incomingPayload )

        self.assertEqual( response.code, 200 )
        self.assertEqual( UserSaveHandler._requestCount, 1 )
        # self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
