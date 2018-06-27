"""
Created by adam on 6/26/18
"""
__author__ = 'adam'

import unittest
# from aiounittest import futurized, AsyncTestCase
# from unittest.mock import Mock, patch
from CommonTools.Loggers.FileLoggers import FileWritingLogger


class FileWritingLogger( unittest.TestCase ):
    def setUp(self):
        self.obj = FileWritingLogger()

    def test_something( self ):
        self.assertEqual( True, True )


if __name__ == '__main__':
    unittest.main()
