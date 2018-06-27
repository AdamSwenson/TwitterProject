"""
Created by adam on 7/5/17
"""
from unittest import TestCase
from TwitterDatabase.DatabaseAccessObjects.Cursors import TweetCursor
from Models.TweetORM import Tweet
__author__ = 'adam'

limit = 50

class TestTweetCursor(TestCase):
    def test__create_iterator(self):

        t = TweetCursor(limit=limit)
        self.assertEqual(t.limit, limit)

    def test_next_tweet(self):
        t = TweetCursor(limit=limit)
        obj = t.next_tweet()
        self.assertIsInstance(obj, Tweet )

    def test_next(self):
        t = TweetCursor(limit=limit)
        obj = t.next()
        self.assertIsInstance(obj, Tweet )

    def test_limit_on(self):
        limit = 5
        t = TweetCursor(limit=limit)
        with self.assertRaises(StopIteration):
            for i in range(0, limit):
                obj = t.next()
                self.assertIsInstance(obj, Tweet )
