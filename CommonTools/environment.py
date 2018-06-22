"""
Created by adam on 11/3/16
"""
__author__ = 'adam'

import os
import sys

############## Locations of code
ROOT = os.getenv( "HOME" )
BASE = '%s/Dropbox/TwitterProject' % ROOT

# Project folder paths
PROJ_BASE = "%s/CommonTools" % BASE

# add everyone to path explicitly
sys.path.append( PROJ_BASE )
