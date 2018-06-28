"""
Created by adam on 6/28/18
"""
__author__ = 'adam'

import json
import environment as env

import asyncio
from Server.ClientSide.Clients import Client
from Server.ServerTools.Routes import USER_ROUTE

TEST_DATA_JSON = "%s/test-user-api-responses" % env.LOG_FOLDER_PATH

if __name__ == '__main__':
    # Load test data
    with open(TEST_DATA_JSON, 'r') as f:
        data = json.load(f)
    url = "%s%s" % (env.DB_URL, USER_ROUTE)
    print(url)
    c = Client(url)


    loop = asyncio.get_event_loop()

    t1 = asyncio.ensure_future(c.send(data))
    # t2 = asyncio.ensure_future(c.async_send_flush_command())
    print('sending')
    loop.run_until_complete(t1)
    #
    # t2 = asyncio.ensure_future(c.async_send_flush_command())
    # print('flushing')
    # loop.run_until_complete(t2)

    loop.close()


    print('done')

