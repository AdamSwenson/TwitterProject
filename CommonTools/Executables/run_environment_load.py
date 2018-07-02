"""
Created by adam on 7/2/18
"""
__author__ = 'adam'
import environment as env
import sys, os

ROOT = os.getenv( "HOME" )
PROJ_ROOT = "%s/Dropbox/PainNarrativesLab/TwitterProject" % ROOT

if __name__ == '__main__':
    print(sys.argv[1])
    print('port is: %s' %env.DB_PORT)

    p = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    print(p)
