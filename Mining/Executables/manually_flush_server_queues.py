"""
Manually sends the flush queues command to the server

Created by adam on 6/30/18
"""
__author__ = 'adam'

import environment as env
from Server.ClientSide.Clients import Client
from Server.ServerTools.Routes import TWEET_ROUTE


def main():
    print( 'Starting call' )
    url = "%s%s" % (env.DB_URL, TWEET_ROUTE)
    c = Client( url )
    print("Sending results to %s " % url)
    c.send_flush_command()
    print( 'done' )


if __name__ == '__main__':
    main()
