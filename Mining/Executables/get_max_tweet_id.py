"""
MOSTLY USED FOR TESTING

Created by adam on 10/3/19
"""
__author__ = 'adam'


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

    url = "%s%s" % (env.DB_URL, TWEET_ROUTE)
    c = Client( url )
    print( "Sending results to %s " % url )

    try:
        print('asking')
        result = await c.get_max_tweet_id()
        r = decode_payload( result.body )
        maxId = r[ 'max_tweet_id' ]
        print(maxId)
    except AttributeError:
        maxId = None
    except Exception as e:
        print(e)


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