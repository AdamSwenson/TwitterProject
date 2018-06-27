"""
Created by adam on 3/27/18
"""
__author__ = 'adam'


from tests.helpers.Factories import UserFactory
from TwitterDatabase.DatabaseAccessObjects.Cursors import Cursor


class DummyUserCursor(Cursor):
    def __init__(self):
        self.item_iterator = self._create_iterator()

    def _create_iterator(self):
        while True:
            u = UserFactory()
            yield u

