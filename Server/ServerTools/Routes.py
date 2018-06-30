"""
Created by adam on 6/25/18
"""
__author__ = 'adam'

from Server.RequestHandlers.WordMapHandlers import WordMapHandler
from Server.RequestHandlers.TweetSaveHandlers import TweetSaveHandler
from Server.RequestHandlers.UserSaveHandlers import UserSaveHandler
from Server.RequestHandlers.DbInfoHandlers import DBInfoHandler

USER_ROUTE = "/users"
TWEET_ROUTE = "/tweets"
WORD_MAP_ROUTE = "/"
DB_INFO_ROUTE = "/info"

route_handlers = [
    (r"%s" % USER_ROUTE, UserSaveHandler),
    (r"%s" % TWEET_ROUTE, TweetSaveHandler),
    (r"%s" % WORD_MAP_ROUTE, WordMapHandler),
    (r"%s" % DB_INFO_ROUTE, DBInfoHandler)
]
