"""
These tools are for use with TweetORM at
version 0.3.0 or higher.
Created by adam on 8/17/18
"""
__author__ = 'adam'

import datetime

import sqlalchemy

from Models.TweetORM import Tweets as Tweet, TweetFactory
from Models.TweetORM import Users as User

TWEET_FIELDS_TO_UPDATE = ('retweeted', 'retweet_count', 'favorite_count')


def get_user_by_id( user_id: int, session: sqlalchemy.orm.Session ):
    """Loads user object from database, given their user id.
    Will return None if no user exists
    :type user_id: int
    :param user_id:
    :type session: sqlalchemy.orm.Session
    """
    return session.query( User ).filter( User.userID == user_id ).first()


def get_tweet_by_id( tweet_id: int, session: sqlalchemy.orm.Session ):
    """Loads tweet object from database, given their tweet id
    :type tweet_id: int
    :param tweet_id:
    :type session: sqlalchemy.orm.Session
    """
    return session.query( Tweet ).filter( Tweet.tweetID == tweet_id ).first()


def update_tweet_if_changed(tweet: Tweet, session):
    """This is called after the tweet object has been created
    and the db throws and IntegrityError. It checks whether
    the tweet has changed and saves it if so
    """
    # existingTweet = get_tweet_by_id(  tweet.tweetID, session )
    session.merge(tweet)

    # # check that actually exists, if not, uh oh
    # if not isinstance(existingTweet, Tweet):
    #     raise sqlalchemy.exc.DatabaseError
    #
    # # We already have the tweet
    # # so we check if it needs updating, if so
    # # we update it
    # isUpdated = False
    # for f in TWEET_FIELDS_TO_UPDATE:
    #     newVal = getattr( tweet, f )
    #     if getattr( existingTweet, f ) != newVal:
    #         # if any of these fields have changed, we
    #         # know to save the changes with audit info
    #         # Because the existingTweet was added to the session
    #         # when we loaded it and the newly created one is not,
    #         # we set the values on the existing one
    #         setattr( existingTweet, f, newVal )
    #         # and set the flag so we know to add the
    #         # audit data etc
    #         if not isUpdated:
    #             isUpdated = True
    # if isUpdated:
    #     # we have to add the audit stuff
    #     # check first that the audit data dict exists
    #     if existingTweet.audit_data is None: existingTweet.audit_data = {}
    #     existingTweet.audit_data[ datetime.datetime.now() ] = { 'event': 'tweet_updated' }
    #     # and save it to the db
    #     # session.add(existingTweet) # presumably redundant
    session.commit()
    return True
    # we return the updated status, so that we can log it
    # return isUpdated


# def create_or_update_tweet( result, session ):
#     # Lookup the tweet to see if we already have it
#     t = get_tweet_by_id( int( result[ 'id_str' ] ), session )
#
#     if isinstance( t, Tweet ):
#
#         # We already have the tweet
#         # so we check if it needs updating, if so
#         # we update it
#         isUpdated = False
#         for f in TWEET_FIELDS_TO_UPDATE:
#             newVal = getattr( tweet, f )
#             if getattr( existingTweet, f ) != newVal:
#                 # set the value
#                 setattr( tweet, f, result[ f ] )
#                 # and set the flag so we know to add the
#                 # audit data etc
#                 if not isUpdated:
#                     isUpdated = True
#         if not isUpdated:
#             # now that we're done checking
#             # if the tweet has not been updated
#             # nothing needs to happen, so we return None
#             return None
#         else:
#             # otherwise we have to add the audit stuff
#             t.audit_data[ datetime.datetime.now() ] = { 'event': 'tweet_updated' }
#             # and return the tweet to be saved
#             return t
#
#     else:
#         # if it doesn't yet exist, create it
#         tweet = TweetFactory( result )
#         # add it to the session
#         session.add( tweet )


if __name__ == '__main__':
    pass
