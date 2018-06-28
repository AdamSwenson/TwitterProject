import unittest

import tornado
from tornado.testing import AsyncHTTPTestCase
from tornado_sqlalchemy import make_session_factory

from Server.RequestHandlers.TweetSaveHandlers import TweetSaveHandler
from tests.helpers.TwitterSearchResultFactories import TweetSearchResultFactory



def serializeTweetResult( result ):
    """The search script returns objects, converts into a dictionary so
    that they can be serialized when we send them to ther server.
      """
    return { k: getattr( result, k ) for k in result.__dict__ }


class TweetSaveHandlersTests( AsyncHTTPTestCase ):
    def get_app( self ):
        factory = make_session_factory( 'sqlite://' )
        return tornado.web.Application( [ (r'/', TweetSaveHandler) ], session_factory=factory )

    def test_post( self ):
        self.numTweets = 30
        self.Tweets = [ serializeTweetResult( TweetSearchResultFactory() ) for _ in range( 0, self.numTweets ) ]
        self.incomingPayload = tornado.escape.json_encode( self.Tweets )  # for u in self.Tweets ]

        # call
        response = self.fetch( '/', method="POST", body=self.incomingPayload )

        self.assertEqual( response.code, 200 )
        self.assertEqual( TweetSaveHandler._requestCount, 1 )
        # self.assertTrue(False)


if __name__ == '__main__':
    unittest.main()
