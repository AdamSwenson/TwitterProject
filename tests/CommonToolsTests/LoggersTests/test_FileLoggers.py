"""
Created by adam on 6/26/18
"""
__author__ = 'adam'
import environment
import unittest
# from aiounittest import futurized, AsyncTestCase
# from unittest.mock import Mock, patch
from CommonTools.Loggers.FileLoggers import FileWritingLogger


class FileWritingLoggerTest( unittest.TestCase ):
    def setUp(self):
        logpath = "%s/twitter-utf-fuckup.txt" % environment.LOG_FOLDER_PATH
        print(logpath)
        self.obj = FileWritingLogger(log_path=logpath)

    def test_something( self ):
        self.obj.log('tacoes')
        self.assertEqual( True, True )


if __name__ == '__main__':
    unittest.main()
