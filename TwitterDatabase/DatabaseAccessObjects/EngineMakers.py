"""
Created by adam on 6/25/18
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

import environment

__author__ = 'adam'


def make_scoped_session_factory( engine ):
    session_factory = sessionmaker( bind=engine )
    return scoped_session( session_factory )


def make_session_factory( engine ):
    return sessionmaker( bind=engine )


def initialize_engine( conn=environment.ENGINE ):
    """Creates the relevant connection engine"""
    if conn is not None:
        method = { 'sqlite': create_sqlite_engine,
                   'sqlite-file': _create_sqlite_file_engine,
                   # 'mysql': _create_mysql_engine,
                   # 'mysql_test': _create_mysql_test_engine
                   }.get( conn )

        engine = method()
        # Base.metadata.create_all( engine )
        return engine

    raise ValueError


def create_sqlite_engine( echo=False ):
    """Creates an in-memory sqlite db engine"""
    conn = 'sqlite:///:memory:'
    print( "creating connection: %s " % conn )
    return create_engine( conn, echo=False )


def sqlite_file_connection_string_generator( folder_path=environment.DB_FOLDER, max_files=environment.MAX_DB_FILES ):
    cnt = 1
    while True:
        file = '%s/wordmapping%s.db' % (folder_path, cnt)
        yield file
        # yield 'sqlite:////%s' % file
        if cnt < max_files:
            cnt += 1
        else:
            cnt = 1


file_path_generator = sqlite_file_connection_string_generator()


def _create_sqlite_file_engine( conn=next( file_path_generator ), echo=True ):
    """Creates an sqlite db engine using the file defined in SQLITE_FILE"""
    print( "creating connection: %s " % conn )
    return create_engine( conn, echo=echo )


# @contextmanager
def session_scope( engine=None ):
    """
    Provide a transactional scope around a series of operations.

    We need a single db connection instance for all of the
    server processes. Otherwise, we will have trouble with
    concurrent writes to the file.
    That's what we create here

    usage:
        with sesssion_scope() as session:
            ...do stuff...
    """
    try:
        if engine is None:
            engine = initialize_engine( environment.ENGINE )
        # DataTools's handle to database at global level
        # SessionFactory = make_scoped_session_factory(engine)
        SessionFactory = make_session_factory( engine )

        if environment.ENGINE == 'sqlite' or environment.ENGINE == 'sqlite-file':
            # We need to get the db into memory when start up
            # environmental variables will determine details of the
            # db
            create_db_tables( engine )

        session = SessionFactory()
        yield session
        session.commit()

    except:
        session.rollback()
        raise

    finally:
        if session:
            session.close()


# def _create_mysql_engine():
#     print( "creating connection: mysql %s" % environment.DB)
#     return create_engine( 'mysql+mysqlconnector://root:''@localhost:3306/%s' % DB )
#
#
# def _create_mysql_test_engine():
#     print( "creating connection: mysql %s" % DB )
#     if DB is 'twitter_wordsTEST':
#         print( "creating connection: mysql twitter_wordsTEST " )
#         return create_engine( 'mysql+mysqlconnector://root:''@localhost:3306/twitter_wordsTEST' )
#
#     return create_engine( "mysql+mysqlconnector://root:''@localhost:3306/%s" % DB )
#
    # return create_engine("mysql+mysqlconnector://root:@localhost/)
