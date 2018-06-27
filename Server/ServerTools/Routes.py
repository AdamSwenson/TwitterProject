"""
Created by adam on 6/25/18
"""
__author__ = 'adam'

import environment
from RequestHandlers.WordMapHandlers import WordMapHandler
from RequestHandlers.TweetSaveHandlers import TweetSaveHandler
from RequestHandlers.UserSaveHandlers import UserSaveHandler

USER_ROUTE = r"/users"
TWEET_ROUTE = r"/tweets"
WORD_MAP_ROUTE = r"/"

route_handlers = [
    (USER_ROUTE, UserSaveHandler),
    (TWEET_ROUTE, TweetSaveHandler),
    (WORD_MAP_ROUTE, WordMapHandler),
]
