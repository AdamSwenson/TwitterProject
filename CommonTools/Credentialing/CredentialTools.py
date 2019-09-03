"""
Tools for loading credentials from a file
Created by adam on 6/21/18
"""
__author__ = 'adam'

import xml.etree.ElementTree as ET


class CredentialLoader( object ):

    def __init__( self, credentials_file ):
        self.credentials = ET.parse( credentials_file )

    def find( self, field ):
        return self.credentials.find( field ).text

    def make_dsn( self, driver ):
        """This is used for alembic because can't make the dsn
        via the usual methods in DataConnections due to the command line
        options not being processed in environment. This shouldn't be used
        for anything else"""
        self._server = self.find( 'db_host' )
        self._port = self.find( 'db_port' )
        if self._port is not None:
            self._port = int( self._port )
        self._username = self.find( 'db_user' )
        # self._db_name = environment.DB
        self._db_name = self.find( 'db_name' )
        self._password = self.find( 'db_password' )
        if self._port:
            server = "%s:%s" % (self._server, self._port)
        else:
            server = self._server
        dsn = "mysql%s://%s:%s@%s/%s?charset=utf8mb4" % (
            driver, self._username, self._password, server, self._db_name)
        return dsn


if __name__ == '__main__':
    pass
