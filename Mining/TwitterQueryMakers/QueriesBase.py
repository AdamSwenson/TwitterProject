"""
Created by adam on 7/31/19
"""
__author__ = 'adam'

from Mining.Miner.TwitterLogin import TwitterConnection


class GetterBase(object):

    def __init__( self, credentials_file ):
        self.credentials_file = credentials_file
        self.make_twitter_connection()

    def make_twitter_connection( self ):
        """Creates a connection to the twitter server.
        This was added to the query object itself in TWIT-57
        to better handle ConnectionResetErrors"""
        connection = TwitterConnection( self.credentials_file )
        self.conn = connection.connection





if __name__ == '__main__':
    pass