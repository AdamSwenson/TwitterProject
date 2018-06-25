"""
Created by adam on 7/6/17
"""
import unittest
import environment
from unittest import TestCase

from TwitterDataAnalysis.DataTools.Cursors import UserCursor
from TwitterDataAnalysis.DataTools.TweetORM import Users

__author__ = 'adam'

language = 'abc'
limit = 50



class TestUserCursor(TestCase):
    def setUp(self):
        self.t = UserCursor(limit=limit, language=language)


    def test__create_iterator(self):
        self.assertEqual(self.t.limit, limit)
        self.assertEqual(self.t.language, language)
        # del t

    def test_next_user(self):
        # t = UserCursor()
        obj = self.t.next_user()
        # del t
        self.assertIsInstance(obj, Users )

    def test_next(self):
        # t = UserCursor()
        obj = self.t.next()
        # del t
        self.assertIsInstance(obj, Users )


if __name__ == '__main__':
    unittest.main()
