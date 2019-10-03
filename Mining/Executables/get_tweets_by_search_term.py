"""
This replaces the existing automine functions
It is is the main search process

Created by adam on 6/28/18
"""
__author__ = 'adam'
import asyncio
from datetime import datetime

from progress.spinner import MoonSpinner

import environment as env
from CommonTools.FileTools import CsvFileTools
from Mining.Miner.TwitterLogin import TwitterConnection
from Mining.TwitterQueryMakers.TwitterQueries import TweetsGetter
from Server.ClientSide.Clients import Client
from Server.ServerTools.Helpers import convert_object_into_dict, decode_payload
from Server.ServerTools.Routes import TWEET_ROUTE


search_terms_file = "%s/tweet-search-terms.csv" % env.EXPERIMENTS_FOLDER

spinner = MoonSpinner()

# How often to update the terminal
NOTICE_LIMIT = 5000


# def make_tweet_searcher(credentials_file):
#     """"Utility to make it easier to recreate a new connection
#      if the original connection gets remotely reset
#      """
#     # Create a connection
#     connection = TwitterConnection( credentials_file )
#
#     # create the object which will execute searches
#     return TweetsGetter( connection )


async def run():
    received_count = 0
    # This will be used to control how often the terminal displays an update on progress
    notice_count = 0

    # Set up the machinery for saving the
    # processed results to our database
    url = "%s%s" % (env.DB_URL, TWEET_ROUTE)
    c = Client( url )
    print( "Sending results to %s " % url )

    # Create connection to twitter and make the object that will
    # execute searches
    searcher = TweetsGetter(env.TWITTER_CREDENTIAL_FILE)

    try:
        result = await c.get_max_tweet_id()
        r = decode_payload( result.body )
        maxId = r[ 'max_tweet_id' ]
    except AttributeError:
        maxId = None
    except Exception as e:
        print(e)

    # load ids to retrieve from file
    searchTerms = CsvFileTools.read_list( search_terms_file )
    try:
        # rate limiting is automatically on, so no need to wait
        while True:
            # try:
            results = searcher.get_tweets_for_search_terms( searchTerms, afterId=maxId )
            # convert each result to a dictionary
            results = [ convert_object_into_dict( result ) for result in results ]
            # except ConnectionResetError as cre:
            #     # Handle the remote twitter server resetting the connection
            #     print("Connection error with remote connection to twitter. \n{}".format(cre))
            #     # Make a new connection and searcher and rerun the search
            #     searcher = make_tweet_searcher(env.TWITTER_CREDENTIAL_FILE)
            #     # Do it again with the same maxId
            #     continue

            # send the results to the server to be saved
            await c.send( results )
            received_count += len( results )
            notice_count += len(results)
            spinner.next()
            # if received_count % 100 == 0:
            if notice_count >= NOTICE_LIMIT:
                print( "                             %s    %s " % (received_count, datetime.now()) )
                notice_count = 0

    except Exception as e:
        # Handles graceful exit after un-anticipated problems
        print( e )
        await c.async_send_flush_command()


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
    main()
