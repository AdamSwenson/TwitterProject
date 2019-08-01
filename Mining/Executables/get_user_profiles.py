"""
Looks up a list of user ids to retrieve, then downloads their profiles. 
It chunks the requests as required and processes the results asynchronously.
Created by adam on 6/22/18
"""
__author__ = 'adam'
import asyncio

import environment as env
from CommonTools.FileTools import CsvFileTools
from Mining.Miner.TwitterLogin import TwitterConnection
from Mining.TwitterQueryMakers.UserQueries import UsersGetter
from Server.ClientSide.Clients import Client
from Server.ServerTools.Routes import USER_ROUTE

IDS_PER_QUERY = 100

user_ids_file = "%s/user-ids-to-download.csv" % env.EXPERIMENTS_FOLDER


def serializeSearchResult( result ):
    """The search script returns objects, converts into a dictionary so
    that they can be serialized when we send them to ther server.
      """
    print( result.__dict__ )
    return { k: getattr( result, k ) for k in result.__dict__ }


# def make_users_searcher( credentials_file ):
#     """"Utility to make it easier to recreate a new connection
#      if the original connection gets remotely reset
#      """
#     # Create a connection
#     connection = TwitterConnection( credentials_file )
#
#     # create the object which will execute searches
#     return UsersGetter( connection )


async def run():
    # Set up the machinery for saving the
    # processed results
    url = "%s%s" % (env.DB_URL, USER_ROUTE)
    c = Client( url )
    print( "Sending results to %s " % url )

    # Create connection to twitter and make the object that will
    # execute searches
    searcher = UsersGetter(env.TWITTER_CREDENTIAL_FILE)

    # load ids to retrieve from file
    userIds = CsvFileTools.read_list_generator( user_ids_file )

    query_ids = [ ]

    while True:

        try:
            for i in range( 0, IDS_PER_QUERY ):
                query_ids.append( next( userIds ) )

            # try:
            results = searcher.get_profiles_for_users( query_ids )
            # Probably don't want to handle this like with the twitter searcher in TWIT-57
            # since it will skip a user id on the next run.
            # except ConnectionResetError as cre:

            # results = [convert_object_into_dict(result ) for result in results]
            # send the results to the server to be saved
            await c.send( results )

        except StopIteration:
            results = searcher.get_profiles_for_users( query_ids )
            await c.send( results )
            await c.async_send_flush_command()
            break


# @log_start_stop( [ environment.RUN_TIME_LOG ], text='no stopwords'  )
def main():
    print( 'Starting run' )
    # start the event loop which will schedule all tasks
    loop = asyncio.get_event_loop()
    t1 = asyncio.ensure_future( run() )
    loop.run_until_complete( t1 )
    loop.close()
    print( 'done' )


if __name__ == '__main__':
    print( 'j' )
    main()
