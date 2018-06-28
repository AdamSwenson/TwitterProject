"""
Created by adam on 6/26/18
"""
import unittest

from TwitterDatabase.Models.TweetORM import UserFactory, User, Users

__author__ = 'adam'
import json

from sqlalchemy import inspect


class UserFactoryTests( unittest.TestCase ):
    def setUp( self ):
        pass

    def test_properly_fills_defined_attributes( self ):
        data = { 'id': 4,
                 'screen_name': 'taco',
                 'id_str': '4',
                 'name': 'dog food',
                 'description': 'loves pets',
                 'lang': 'bark' }
        # call
        result = UserFactory( data )

        # check
        self.assertIsInstance(result, User, 'result is correct type')
        for key in data.keys():
            self.assertEqual( getattr( result, key ), data[ key ], "%s was set on object" % key )

        self.assertEqual(getattr(result, 'userID'), data['id'], "userID was set from the incoming id")

    def test_stores_undefined_attributes_to_json( self ):
        defined_data = { 'id': 4,
                     'screen_name': 'taco',
                     'id_str': '4',
                     'name': 'dog food',
                     'description': 'loves pets',
                     'lang': 'bark' }
        undefined_data = { 'taco_fun_day': 'tuesday', 'dog_park_locations': 5}
        data = {**defined_data, **undefined_data}

        # call
        result = UserFactory( data )

        # check
        self.assertIsInstance(result, User, 'result is correct type')

        for key in defined_data.keys():
            self.assertEqual( getattr( result, key ), defined_data[ key ], "%s was set on object" % key )

        self.assertEqual(getattr(result, 'userID'), data['id'], "userID was set from the incoming id")

        # Check the undefined stuff
        od = getattr( result, 'other_data' )
        od = json.loads(od)
        for key in undefined_data.keys():
            self.assertEqual(od[key], undefined_data[ key ], "%s was set in other_data" % key )

    if __name__ == '__main__':
        unittest.main()
