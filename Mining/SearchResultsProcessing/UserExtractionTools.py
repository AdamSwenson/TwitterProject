"""
In the laptop miner, we've been storing the tweet's user
in the other_data json column. These are tools for handling
that data or updating the users table from such data

Created by adam on 8/16/18
"""
__author__ = 'adam'

import json

import sqlalchemy

from TwitterDatabase.Models.TweetORM import Tweet
from TwitterDatabase.Models.TweetORM import UserFactory
from TwitterDatabase.Models.TweetORM import Users as User

"""Database fields which should be updated if they have changed"""
USER_FIELDS_TO_UPDATE = ('friends_count', 'followers_count', 'statuses_count')


# ----------------- Database tools
def tweets_with_other_data_generator( session:  sqlalchemy.orm.Session ):
    """Returns an iterator which yields tweets that have a non-empty other_data field
    :type session: sqlalchemy.orm.Session
    """
    for tweet in session.query( Tweet ).filter( Tweet.other_data.isnot( None ) ):
        yield tweet


def get_user_by_id( user_id: int, session: sqlalchemy.orm.Session ):
    """Loads user object from database, given their user id
    :type user_id: int
    :param user_id:
    :type session: sqlalchemy.orm.Session
    """
    return session.query( User ).filter( User.userID == user_id ).first()


# ----------------- Actual extraction tools
def extract_user_dict_from_tweet( tweet: Tweet ):
    """Takes the other_data field from a tweet object and
    extracts the data for the user from it.
    It returns a dictionary rather than a User model object
    because we might want to try looking up whether the user
    exists before creating a new user object.

    :type tweet Tweet
    :returns dict
    """
    if tweet.other_data and len( tweet.other_data ) > 0:
        # extract the json into a dict
        j = json.loads( tweet.other_data )
        # extract the user json from the created dict
        return json.loads( j[ 'user' ] )


def update_or_create_user_from_tweet( tweet: Tweet, session: sqlalchemy.orm.Session ):
    """Extracts the user data from the tweet's other_data json field
    and saves a user object. If there already is a user with that id, it
    updates their properties. Otherwise, it creates a new user object
    :type session:  sqlalchemy.orm.Session
    :param session: session object to perform queries with
    :type tweet: Tweet
    :returns User
    """

    data = extract_user_dict_from_tweet( tweet )

    if data is not None:

        # Try to load existing user
        userId = tweet.userID
        user = get_user_by_id( userId, session )

        if user is None:
            # make user from the json
            user = UserFactory( data )
            user.audit_data = { 'created_from_tweet': tweet.tweetID }
            # the new object isn't yet tracked, so we need to add it to the session
            session.add(user)
        else:
            # make a copy, we need to be a bit sneaky because sqlalchemy isn't watching the json field
            # but it will freak out over a Detached Instance
            j = { k: user.audit_data[ k ] for k in user.audit_data.keys() }
            # update relevant fields
            audit = { 'event': 'update_from_tweet', 'tweetId': tweet.tweetID }
            for f in USER_FIELDS_TO_UPDATE:
                setattr( user, f, data[ f ] )
                audit[ f ] = data[ f ]
            j[ tweet.tweetID ] = audit
            user.audit_data = j

            # return the object in case needed
        return user


def harvest_users_from_tweets( session: sqlalchemy.orm.Session, FLUSH_LIMIT=10, startTweet=None ):
    """This iterates through tweets from the database and harvests user data from them"""
    users = 0
    lastTweetId = None

    tweetIter = tweets_with_other_data_generator( session )

    try:
        while True:
                tweet = next( tweetIter )
                user = update_or_create_user_from_tweet( tweet, session )

                users += 1
                lastTweetId = tweet.tweetID

                if users % FLUSH_LIMIT == 0:
                    print( 'flushing at %s users' % users )
                    session.commit()

    except StopIteration:
        print( "%s users created or updated" % users )
        session.commit()

    finally:
        print("Last processed tweet %s" % lastTweetId)
        # session.commit()
        session.close()


if __name__ == '__main__':
    pass
#     dao = DC.MySqlConnection( environment.CREDENTIAL_FILE )
#     Session = sessionmaker( bind=dao.engine )
#
# session = Session()
#
# # Testing updates
#
# session = Session()
#
# u = session.query( User ).filter( User.screen_name == 'Adam' ).first()
#
# assert (u is not None)
#
# u.add_tweet_update_info_to_audit_data( { 'jip': 'j' } )
#
# j = { k: u.audit_data[ k ] for k in u.audit_data.keys() }
