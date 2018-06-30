"""
Created by adam on 11/6/16
"""
from DatabaseAccessObjects.EngineMakers import create_sqlite_engine

__author__ = 'adam'

from CommonTools.Credentialing.CredentialTools import CredentialLoader
from CommonTools.Utilities.Decorators import deprecated

# import MySQLdb
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session

import environment
from environment import *

# Base class that maintains the catalog of tables and classes in db
Base = declarative_base()


class Connection( object ):
    """
    Parent class for creating sqlalchemy engines, session objects,
    and other db interaction stuff behind the scenes from a file
    holding credentials

    Attributes:
        engine: sqlalchemy engine instance
        session: sqlalchemy local session object. This is the property that should do most work
        _credential_file: String path to file with db connection info
        _username: String db username
        _password: String db password
        _server: String db server
        _port: db port
        _db_name: String name of db
    """

    def __init__( self, credential_file=None, create_engine=True ):
        """
        Loads db connection credentials from file and returns a mysql sqlalchemy engine
        Args:
            :param credential_file: String path to the credential file to use
        Returns:
            :return: sqlalchemy.create_engine Engine instance
        """
        self._credential_file = credential_file
        self._load_credentials()

        # We have the option of not creating the engine for when
        # we need to use the dsn with a scoped session
        if create_engine:
            self._make_engine()

    def _load_credentials( self ):
        """
        Opens the credentials file and loads the attributes
        """
        if self._credential_file is not None:
            credentials = CredentialLoader( self._credential_file )

        # credentials = ET.parse( self._credential_file )
            self._server = credentials.find( 'db_host' )
            self._port = credentials.find( 'db_port' )
            if self._port is not None:
                self._port = int( self._port )
            self._username = credentials.find( 'db_user' )
            # self._db_name = environment.DB
            self._db_name = credentials.find( 'db_name' )
            self._password = credentials.find( 'db_password' )

    def _make_engine( self ):
        """
        Creates the sqlalchemy engine and stores it in self.engine
        """
        raise NotImplementedError


class MySqlConnection( Connection ):
    """
    Uses the MySQL-Connector-Python driver (pip install MySQL-Connector-Python driver)
    """

    def __init__( self, credential_file, create_engine=True ):
        self._driver = '+mysqlconnector'
        super( __class__, self ).__init__( credential_file , create_engine)

    def make_dsn( self ):
        """Creates the database connection url for the mysql database. It sets the
        value internally but also returns it so that it can be used independently
        """
        if self._port:
            server = "%s:%s" % (self._server, self._port)
        else:
            server = self._server
            self._dsn = "mysql%s://%s:%s@%s/%s" % (self._driver, self._username, self._password, server, self._db_name)
            print(self._dsn)
            return self._dsn

    def _make_engine( self ):
        self.make_dsn()
        self.engine = create_engine( self._dsn )


class SqliteFileConnection( Connection ):
    """
    Makes a connection to a file-based sqlite database.
    Note that does not actually populate the database. That
    requires a call to: Base.metadata.create_all(SqliteConnection)
    """

    def __init__( self ):
        super().__init__()

    def _make_engine( self ):
        self.engine = create_engine( 'sqlite:%s' % SQLITE_FILE, echo=False )


class SqliteConnection( Connection ):
    """
    Makes a connection to an in memory sqlite database.
    Note that does not actually populate the database. That
    requires a call to: Base.metadata.create_all(SqliteConnection)
    """

    def __init__( self ):
        super().__init__()

    def _make_engine( self ):
        self.engine = create_sqlite_engine()
        # create_engine( 'sqlite:///:memory:', echo=True )


class BaseDAO( object ):
    """
    Parent class for database interactions.
    The parent will hold the single global connection (i.e. sqlalchemy Session)
    to the db.
    Instance classes will have their own session instances
    Attributes:
        global_session: (class attribute) A sqlalchemy configurable sessionmaker factory (sqlalchemy.orm.session.sessionmaker)
            bound to the engine. Is not itself a session. Instead, it needs to be instantiated: DAO.global_session()
        engine: sqlalchemy.engine.base.Engine instance
    """
    global_session = None

    def __init__( self, engine ):
        assert (isinstance( engine, sqlalchemy.engine.base.Engine ))
        self.engine = engine
        if BaseDAO.global_session is None:
            BaseDAO._create_session( engine )

    @staticmethod
    def _create_session( engine ):
        """
        Instantiates the sessionmaker factory into the global_session attribute
        """
        BaseDAO.global_session = sqlalchemy.orm.sessionmaker( bind=engine )


class DAO( BaseDAO ):
    """
    example instance. Need to use metaclass to ensure that
    all instances of DAO do this
    """

    def __init__( self, engine ):
        assert (isinstance( engine, sqlalchemy.engine.base.Engine ))
        super().__init__( engine )
        self.session = BaseDAO.global_session()


class NonOrmMySqlConnection( Connection ):

    @deprecated
    def __init__( self, credential_file ):
        self._driver = '+mysqlconnector'
        super( __class__, self ).__init__( credential_file )

    def _make_engine( self ):
        if self._port:
            server = "%s:%s" % (self._server, self._port)
        else:
            server = self._server
        # self.engine = MySQLdb.connect( server, self._username, self._password, self._db_name,
        #                                cursorclass=MySQLdb.cursors.DictCursor )


if __name__ == '__main__':
    pass
    # # connect to db
    # engine = initialize_engine()
    # # DataTools's handle to database at global level
    # Session = sessionmaker( bind=engine )
