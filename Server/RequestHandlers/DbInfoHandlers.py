"""
Created by adam on 6/28/18
"""
__author__ = 'adam'

# Loggers and instrumentation
from Server.RequestHandlers.HandlerParent import IRequestHandler
from TwitterDatabase.Models.TweetORM import Tweets
from Server.ServerTools.Helpers import encode_payload

class DBInfoHandler( IRequestHandler ):

    def get( self ):
        """Get the max tweet id"""
        with self.make_session() as session:
            query = session.query( Tweets ).order_by( Tweets.tweetID )
            result = query.first()
            try:
                print( result.tweetID )
                pl = encode_payload( { 'max_tweet_id': result.tweetID })
            except AttributeError:
                pl = encode_payload( { 'max_tweet_id': None })
            self.write( pl )
