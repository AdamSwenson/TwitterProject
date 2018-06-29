"""
Created by adam on 6/27/18
"""

__author__ = 'adam'

from unittest import TestCase
from TwitterMining.TwitterQueryMakers.UserQueries import UsersGetter, make_query_to_get_users_profiles, make_query_to_get_users_tweets

class queriesTest( TestCase ):

    def test_make_query_to_get_users_profiles( self ):
        ids = [1, 2, 3, 4]
        expect = "user_id=1,2,3,4"
        #call
        result = make_query_to_get_users_profiles(ids)
        # check
        self.assertEqual(expect, result)
