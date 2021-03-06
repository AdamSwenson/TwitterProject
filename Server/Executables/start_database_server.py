"""
Runs the database server which listens for requests containing data to save to the
database.

Created by adam on 3/27/18
"""

__author__ = 'adam'

import sys

import tornado

import environment
from Server.RequestHandlers.WordMapHandlers import WordMapHandler
from Server.RequestHandlers.TweetSaveHandlers import TweetSaveHandler
from Server.RequestHandlers.UserSaveHandlers import UserSaveHandler
from Server.ServerTools.Routes import route_handlers
from Server.ServerTools.ServerExceptions import ShutdownCommanded


def make_sqlalchemy_app():
    from TwitterDatabase.DatabaseAccessObjects.DataConnections import MySqlConnection
    from tornado_sqlalchemy import make_session_factory
    print("Starting sqlalchemy app")

    # We are just going to need the dsn
    conn = MySqlConnection(environment.CREDENTIAL_FILE,  create_engine=False )
    dsn = conn.make_dsn()
    print(dsn)
    factory = make_session_factory( dsn )
    return tornado.web.Application( route_handlers, session_factory=factory )


def make_non_orm_app():
    print("Starting non-orm app")
    return tornado.web.Application( route_handlers )


def make_app():
    if environment.WHICH_SERVER == 'orm':
        print(" \n starting orm")
        return make_sqlalchemy_app()
    if environment.WHICH_SERVER == 'non-orm':
        return make_non_orm_app()


def main():
    print( 'running database server main on port %s' % environment.DB_PORT )
    try:
        app = make_app()
        try:
            sockets = tornado.netutil.bind_sockets( environment.DB_PORT )
        except OSError:
            # In case I've left the port bound up with another process,
            # try reconnecting through a new socket once
            sockets = tornado.netutil.bind_sockets( environment.DB_PORT - 1)
        tornado.process.fork_processes( 0 )  # Forks multiple sub-processes
        server = tornado.httpserver.HTTPServer( app )
        server.add_sockets( sockets )
        print( "Listening on %s" % environment.DB_PORT )
        # Enter loop and listen for requests
        # NB this is a wrapper around the asyncio loop for the thread
        tornado.ioloop.IOLoop.current().start()

    except ShutdownCommanded as e:
        print( 'dsg received shutdown' )
        WordMapHandler.save_queued()
        sys.exit( 0 )

    except KeyboardInterrupt:
        # print("%s still in queue" % len(WordMapHandler.results))
        # WordMapHandler.save_queued()
        # print("%s in queue after flush" % len(WordMapHandler.results))
        num = TweetSaveHandler._requestCount + WordMapHandler._requestCount + UserSaveHandler._requestCount
        print( "%s requests received" % num)

    finally:
        # WordMapHandler.save_queued()
        pass
        # session.commit()


if __name__ == "__main__":
    main()
