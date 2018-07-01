"""
This replaces the existing automine functions

Created by adam on 6/28/18
"""
__author__ = 'adam'
import asyncio
import sys

import environment as env
from CommonTools.FileTools import CsvFileTools
from Server.ClientSide.Clients import Client
from Server.ServerTools.Routes import TWEET_ROUTE
from Mining.Miner.TwitterLogin import TwitterConnection
from Mining.TwitterQueryMakers.TwitterQueries import TweetsGetter
from Server.ServerTools.Helpers import convert_object_into_dict, decode_payload

from progress.spinner import MoonSpinner

search_terms_file = "%s/tweet-search-terms.csv" % env.EXPERIMENTS_FOLDER

async def run(  ):
    received_count = 0
    spinner = MoonSpinner()

    # Set up the machinery for saving the
    # processed results
    url = "%s%s" % (env.DB_URL, TWEET_ROUTE)
    c = Client( url )
    print("Sending results to %s " % url)

    # Create a connection
    connection = TwitterConnection( env.TWITTER_CREDENTIAL_FILE )

    # create the object which will execute searches
    searcher = TweetsGetter( connection )

    try:
        result = await c.get_max_tweet_id()
        r = decode_payload(result.body)
        maxId = r['max_tweet_id']
    except AttributeError:
        maxId = None

    # load ids to retrieve from file
    searchTerms = CsvFileTools.read_list( search_terms_file )
    try:
        # rate limiting is automatically on, so no need to wait
        while True:
            results = searcher.get_tweets_for_search_terms(  searchTerms , afterId=maxId )
            # convert each result to a dictionary
            results = [convert_object_into_dict(result) for result in results]

            # send the results to the server to be saved
            await c.send(results)
            received_count += len(results)
            spinner.next()
            # print(received_count)
    except Exception as e:
        print(e)
        await c.async_send_flush_command()


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
