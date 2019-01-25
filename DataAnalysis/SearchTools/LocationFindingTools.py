"""
Tools for finding the user's location
based on the extremely variable 'location' field

Created by adam on 1/15/19
"""
__author__ = 'adam'
import pandas as pd

import environment


class Done( Exception ):
    pass


class StateCityFinder( object ):
    def __init__( self, filepath=environment.DATA_FOLDER ):
        # load state names and abbreviations
        state_abbreviations_file = "%s/us-states.csv" % filepath
        self.state_abbrevs = pd.read_csv( state_abbreviations_file )
        self.state_abbrevs.State = self.state_abbrevs.apply( lambda x: x.State.upper().strip(), axis=1 )
        self.city_aliases = {
            'NEW YORK CITY': { 'state': 'NY', 'city': 'New York' },
            'NYC': { 'state': 'NY', 'city': 'New York' }
        }
        # load city data
        cities_file = "%s/us-cities.csv" % environment.DATA_FOLDER
        self.cities = pd.read_csv( cities_file )
        self.cities.city = self.cities.apply( lambda x: x.city.upper().strip(), axis=1 )
        self.cities.state = self.cities.apply( lambda x: x.state.upper().strip(), axis=1 )
        self.cities.set_index( 'city', inplace=True )

    def _lookup_abbrev( self, to_lookup ):
        try:
            v = to_lookup.strip().upper()
            r = self.state_abbrevs[ self.state_abbrevs.Abbreviation == v ]
            return r.Abbreviation.values[ 0 ]
        except:
            pass

    def _lookup_statename( self, to_lookup ):
        try:
            v = to_lookup.strip().upper()
            r = self.state_abbrevs[ self.state_abbrevs.State == v ]
            return r.Abbreviation.values[ 0 ]
        except:
            pass

    def _get_state( self, to_lookup ):
        """Given a string which may contain the state,
        this looks up the abbreviation"""
        # Look for things like: AZ
        # The split handles cases where other crap is appended to the string: 'AZ 🇺🇸'
        s = self._lookup_abbrev( to_lookup.strip().split( ' ' )[ 0 ] )
        if s is None:
            # Look for things like: Arizona
            s = self._lookup_statename( to_lookup )
        if s is None:
            # This handles the full state name in the second position
            # with crap appended : 'Phoenix, Arizona 🇺🇸'
            s = self._lookup_statename( to_lookup.strip().split( ' ' )[ 0 ] )
        return s

    def _detect_comma_separated( self, location_string ):
        """Covers cases: 'Wichita, Kansas',
             'Washington, DC',
             'Phoenix, AZ 🇺🇸',
            'Olney, Maryland, USA'
            """
        try:
            result = { 'city': None, 'state': None }
            locs = location_string.split( ',' )
            if len( locs ) == 1:
                r1 = self._get_state( locs[ 0 ] )
                if r1:
                    result[ 'state' ] = r1
                    raise Done()
            else:
                r2 = self._get_state( locs[ 1 ] )
                if r2:
                    result[ 'state' ] = r2
                    result[ 'city' ] = locs[ 0 ]
                    raise Done()
                # 'Georgia, USA'
                # We do in this order so as to avoid problems with
                # Washington, DC and New York, NY
                r3 = self._get_state( locs[ 0 ] )
                if r3:
                    result[ 'state' ] = r3
                    raise Done()
        except Done:
            return result

    def _detect_space_separated( self, location_string ):
        """ ('Northern Virginia', {'state': 'VA', 'city': None}),
        ('Wichita Kansas',  {'state': 'KS', 'city': 'Wichita'})
        ('San Francisco CA',  {'state': 'CA', 'city': 'San Francisco'})
        """
        result = { 'city': None, 'state': None }
        locs = location_string.split( ' ' )
        try:
            if len( locs ) == 1:
                r1 = self._get_state( locs[ 0 ] )
                if r1:
                    result[ 'state' ] = r1
                    raise Done()
            else:
                r2 = self._get_state( locs[ 1 ] )
                if r2:
                    result[ 'state' ] = r2
                    result[ 'city' ] = locs[ 0 ]
                    raise Done()
                # 'Georgia, USA'
                # We do in this order so as to avoid problems with
                # Washington, DC and New York, NY
                r3 = self._get_state( locs[ 0 ] )
                if r3:
                    result[ 'state' ] = r3
                    raise Done()
        except Done:
            return result

    def _detect_major_city( self, to_lookup ):
        """NB, this may overstate the location of these cities in the resulting data"""
        result = { 'city': None, 'state': None }
        try:
            v = to_lookup.strip().upper()
            r = self.cities.loc[ v ]
            result[ 'city' ] = to_lookup
            result[ 'state' ] = self._lookup_statename( r.state )
            return result
        except:
            return self.city_aliases.get( v )

    def _detect_locale( self, to_lookup ):
        """Northern"""
        locales = [ 'NORTHERN', 'SOUTHERN', 'EASTERN', 'WESTERN', 'CENTRAL' ]
        try:
            # split on space
            locs = to_lookup.split( ' ' )
            locs = [ l.strip().upper() for l in locs ]
            if locs[ 0 ] in locales:
                r = self._get_state( locs[ 1 ])
                if r:
                    return {'city': None, 'state': r}
        except:
            pass

    def parse_location_field( self, location_string ):
        """Main method"""
        result = self._detect_comma_separated( location_string )
        if result is None:
            result = self._detect_space_separated( location_string )
        if result is None:
            result = self._detect_major_city( location_string )
        if result is None:
            result = self._detect_locale( location_string )
        return result


if __name__ == '__main__':
    pass
