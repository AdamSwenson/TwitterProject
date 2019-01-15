"""
Created by adam on 1/15/19
"""
import unittest

__author__ = 'adam'

from DataAnalysis.SearchTools.LocationFindingTools import CityFinder

testcases_commas = [
    # Comma separated
    ('Wichita, Kansas', { 'state': 'KS', 'city': 'Wichita' }),
    ('Washington, DC', { 'state': 'DC', 'city': 'Washington' }),
    ('Washington, District of Columbia', { 'state': 'DC', 'city': 'Washington' }),
    ('New York, NY', { 'state': 'NY', 'city': 'New York' }),
    ('Georgia, USA', { 'state': 'GA', 'city': None }),
    # nb, there's an emoji here which may not be visible on some themes
    ('Phoenix, AZ 🇺🇸', { 'state': 'AZ', 'city': 'Phoenix' }),
    ('Phoenix, Arizona 🇺🇸', { 'state': 'AZ', 'city': 'Phoenix' }),
    ('Olney, Maryland, USA', { 'state': 'MD', 'city': 'Olney' }),
    ('Joshtown, West Virginia, USA', { 'state': 'WV', 'city': 'Joshtown' }),
]

# Space separated
testcases_spaces = [
    ('Wichita Kansas', { 'state': 'KS', 'city': 'Wichita' }),
]

# State only
testcases_state_only = [
    ('Kansas', { 'state': 'KS', 'city': None }),
    ('West Virginia', { 'state': 'WV', 'city': None }),
    ('KS', { 'state': 'KS', 'city': None }),
]

# City only
testcases_city_only = [
    ('Seattle', { 'state': 'WA', 'city': 'Seattle' }),
    ('New York City', { 'state': 'NY', 'city': 'New York' }),
    ('NYC', { 'state': 'NY', 'city': 'New York' }),
]

# General locale
testcases_locales = [
    ('Northern Virginia', { 'state': 'VA', 'city': None }),
    ('Central NJ, USA', { 'state': 'NJ', 'city': None }),
    ('No-Cen. Phoenix, AZ', { 'state': 'AZ', 'city': 'Phoenix' })
]
# Multiple
#             ('DC | Frederick, MD | Chicago'),
#             ('Boston/Providence')]

# disambiguate Los angeles and lousiana (LA)

alltests = testcases_commas + testcases_spaces + testcases_state_only + testcases_city_only + testcases_locales


class TestCityFinder( unittest.TestCase ):

    def test__lookup_abbrev( self ):
        cf = CityFinder()
        self.assertEqual( cf._lookup_abbrev( 'AZ' ), 'AZ' )
        self.assertEqual( cf._lookup_abbrev( 'az' ), 'AZ' )

    def test__lookup_statename( self ):
        cf = CityFinder()
        self.assertEqual( cf._lookup_statename( 'Arizona' ), 'AZ' )
        self.assertEqual( cf._lookup_statename( 'arizona' ), 'AZ' )
        self.assertEqual( cf._lookup_statename( 'ARIZONA' ), 'AZ' )

    def test__get_state( self ):
        cf = CityFinder()
        self.assertEqual( cf._lookup_abbrev( 'AZ' ), 'AZ' )
        self.assertEqual( cf._lookup_abbrev( 'az' ), 'AZ' )
        self.assertEqual( cf._lookup_statename( 'Arizona' ), 'AZ' )
        self.assertEqual( cf._lookup_statename( 'arizona' ), 'AZ' )
        self.assertEqual( cf._lookup_statename( 'ARIZONA' ), 'AZ' )

    def test__detect_comma_separated( self ):
        cf = CityFinder()
        for t in testcases_commas:
            self.assertEqual( t[ 1 ], cf._detect_comma_separated( t[ 0 ] ) )

    def test__detect_space_separated( self ):
        cf = CityFinder()
        for t in testcases_spaces:
            self.assertEqual(t[ 1 ], cf._detect_space_separated( t[ 0 ] ) )

    def test__detect_major_city( self ):
        cf = CityFinder()
        for t in testcases_city_only:
            self.assertEqual( t[ 1 ], cf._detect_major_city( t[ 0 ] ) )

    def test__detect_locale( self ):
        cf = CityFinder()
        for t in testcases_locales:
            self.assertEqual(t[ 1 ], cf._detect_locale( t[ 0 ] )  )

    def test_parse_location_field( self ):
        cf = CityFinder()
        for t in alltests:
            msg = "Expected {}; Received: {}".format(cf.parse_location_field( t[ 0 ] ), t[ 1 ])
            self.assertEqual( t[ 1 ], cf.parse_location_field( t[ 0 ] ))


if __name__ == '__main__':
    unittest.main()
