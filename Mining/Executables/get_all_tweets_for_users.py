"""
Looks up a list of user ids to retrieve, then downloads their profiles. 
It chunks the requests as required and processes the results asynchronously.
Created by adam on 6/22/18
"""
__author__ = 'adam'
import asyncio
import sys

import environment as env
from CommonTools.FileTools import CsvFileTools
from Server.ClientSide.Clients import Client
from Server.ServerTools.Routes import TWEET_ROUTE
from Mining.Miner.TwitterLogin import TwitterConnection
from Mining.TwitterQueryMakers.UserQueries import UsersGetter
from Server.ServerTools.Helpers import convert_object_into_dict


user_ids_file = "%s/user-ids-to-download.csv" % env.EXPERIMENTS_FOLDER

async def run(  ):
    # Set up the machinery for saving the
    # processed results
    url = "%s%s" % (env.DB_URL, TWEET_ROUTE)
    c = Client( url )
    print("Sending results to %s " % url)

    # Create a connection
    connection = TwitterConnection( env.TWITTER_CREDENTIAL_FILE )

    # create the object which will execute searches
    searcher = UsersGetter( connection )

    # load ids to retrieve from file
    userIds = CsvFileTools.read_list_generator( user_ids_file )


    while True:
        try:
            userId = next(userIds)
            results = searcher.get_tweets_for_user( userId )
            # convert each result to a dictionary
            results = [convert_object_into_dict(result) for result in results]
            # print(results)

            # send the results to the server to be saved
            await c.send(results)

        except StopIteration:
            await c.async_send_flush_command()
            break


# @log_start_stop( [ environment.RUN_TIME_LOG ], text='no stopwords'  )
def main():
    print( 'Starting run' )
    # start the event loop which will schedule all tasks
    loop = asyncio.get_event_loop()
    t1 = asyncio.ensure_future( run(  ) )
    loop.run_until_complete( t1 )
    loop.close()
    print( 'done' )


if __name__ == '__main__':
    print('j')
    main()
