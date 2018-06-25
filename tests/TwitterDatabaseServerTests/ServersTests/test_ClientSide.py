import unittest
from aiounittest import futurized, AsyncTestCase
from unittest.mock import Mock, patch


class ClientSideTests( unittest.TestCase ):
    def setUp(self):
        pass

    def test_something( self ):
        self.assertEqual( True, True )


if __name__ == '__main__':
    unittest.main()
