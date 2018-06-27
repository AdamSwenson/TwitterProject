"""
This defines global variables for testing.

Most importantly, this exposes settings.Session
which is the scoped session maker for anything
needing to use sqlalchemy's session for testing

Usage for factories
# Use the not-so-global scoped_session
    # Warning: DO NOT USE common.Session()!
    sqlalchemy_session = settings.Session


Created by adam on 6/27/18
"""
__author__ = 'adam'


from sqlalchemy import orm, create_engine
Session = orm.scoped_session(orm.sessionmaker())

# an Engine, which the Session will use for connection
# resources
engine = create_engine( 'sqlite://' )

# create a configured "Session" class
Session.configure(bind=engine )
