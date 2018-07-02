import unittest
import sys, os
from unittest.mock import patch

ROOT = os.getenv( "HOME" )
PROJ_ROOT = "%s/Dropbox/PainNarrativesLab/TwitterProject" % ROOT


class EnvironmentTest( unittest.TestCase ):
    def test_that_unit_test_loads_correct_config( self ):

        expectedConfig = '%s/configurations/unit-testing.config.ini' % PROJ_ROOT
        testargs = ['', '--config', 'unit-testing']
        with patch.object(sys, 'argv', testargs):
            print(sys.argv)
            import environment
            import environment as env

            self.assertEqual( env.configFile, expectedConfig )


if __name__ == '__main__':
    unittest.main()
