"""
Tools for loading credentials from a file
Created by adam on 6/21/18
"""
__author__ = 'adam'

import xml.etree.ElementTree as ET


class Credentials( object ):

    def __init__( self, credentials_file ):
        self.credentials = ET.parse( credentials_file )
    
    def find( self, field ):
        return self.credentials.find( field ).text


if __name__ == '__main__':
    pass
