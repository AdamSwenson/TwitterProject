"""
Created by adam on 6/28/18
"""
__author__ = 'adam'

from datetime import datetime

from http.client import RemoteDisconnected
from Mining.TwitterQueryMakers.QueriesBase import GetterBase


def make_query( terms ):
    """
    >>>terms =['pain', 'fibromyalgia', 'migraine']
    >>>assert make_query(terms) == "l=en&q=pain%2C OR fibromyalgia%2C OR migraine"
    :return:
    """
    seperator = '%2C OR '
    stem = "l=en&q="

    # not sure if order matters, but just in case....
    # terms = shuffle( terms )

    last = terms[ -1: ][ 0 ]

    for term in terms:
        stem += "%s" % term
        if term != last:
            stem += seperator
    return stem


class TweetsGetter( GetterBase ):

    def __init__( self, credentials_file ):
        super().__init__( credentials_file )

    def get_tweets_for_search_terms( self, search_terms: list, beforeId=None, afterId=None ):
        """
        Returns tweet objects for the given user
        :param search_terms:
        :param beforeId:
        :param afterId:
        :return: list
        """
        query = make_query( search_terms )
        results = [ ]
        for term in search_terms:
            try:
                results += self.conn.GetSearch( term=term, max_id=beforeId, lang='en', since_id=afterId )
            except (ConnectionResetError, RemoteDisconnected) as cre:
                # Handle the remote twitter server resetting the connection
                print( "Connection error with remote connection to twitter. {} \n{}".format( datetime.now(), cre ) )
                # Make a new connection and rerun the search
                self.make_twitter_connection()
                results += self.conn.GetSearch( term=term, max_id=beforeId, lang='en', since_id=afterId )
                # If it fails this time, we won't catch the error

        # results = self.conn.GetSearch( raw_query=query, max_id=beforeId, lang='en', since_id=afterId )
        return [ r._json for r in results ]


if __name__ == '__main__':
    pass
