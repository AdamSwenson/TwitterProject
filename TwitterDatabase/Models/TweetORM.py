"""
This contains classes for loading tweet data

In the process of being converted to use sqlalchemy
"""
from sqlalchemy import Table, Column, ForeignKey, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import inspect

import datetime
from sqlalchemy.sql import func

# import DatabaseAccessObjects.EngineMakers
# from DatabaseAccessObjects import DataConnections
import json
# connecting to db

# Base class that maintains the catalog of tables and classes in db
Base = declarative_base()


class Users(Base):
    __tablename__ = 'users'
    # indexer = Column(Integer, unique=True)
    userID = Column(Integer, primary_key=True, autoincrement=False)
    screen_name = Column(String(225))
    id_str = Column(String(225))
    name = Column(String(225))
    description = Column(String(250))
    lang = Column(String(100))
    utc_offset = Column(String(100))
    verified = Column(String(100))
    followers_count = Column(Integer)
    friends_count = Column(Integer)
    url = Column(String(100))
    time_zone = Column(String(100))
    created_at = Column(String(100))
    entities = Column(String(225))
    favourites_count = Column(Integer)
    statuses_count = Column(Integer)
    id = Column(String(225))
    location = Column(String(225))
    is_translation_enabled = Column(String(10))
    other_data = Column(JSON())
    record_created = Column(DateTime, server_default=func.now())
    record_updated = Column(DateTime, onupdate=datetime.datetime.now)
    audit_data = Column(JSON())

    def item_type( self ):
        return 'user'

    def to_dict( self ):
        mapper = inspect(Users)
        return { column.key : getattr(self, column.key) for column in mapper.attrs}


class Hashtags(Base):
    __tablename__ = 'hashtags'
    # Here we define columns for the table hashtags
    # Notice that each column is also a normal Python instance attribute.
    tagID = Column(Integer, primary_key=True)
    hashtag = Column(String(100), nullable=False)
    # record_created = Column(DateTime, server_default=func.now())
    # record_updated = Column(DateTime, onupdate=func.now())


class Tweets(Base):
    __tablename__ = 'tweets'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    tweetID = Column(Integer, primary_key=True, autoincrement=False)
    userID = Column(Integer) #, ForeignKey('users.userID'))
    tweetText = Column(String(250))
    favorite_count = Column(Integer)
    source = Column(String(250), nullable=False)
    retweeted = Column(String(10))
    retweet_count = Column(Integer)
    in_reply_to_screen_name = Column(String(100))
    favorited = Column(String(10))
    lang = Column(String(100))
    created_at = Column(String(100))
    profile_background_tile = Column(String(100))
    is_translation_enabled = Column(String(100))
    profile_location = Column(String(100))
    other_data = Column(JSON())
    record_created = Column(DateTime,  server_default=func.now())
    record_updated = Column(DateTime,  onupdate=datetime.datetime.now)
    audit_data = Column(JSON())

    def item_type( self ):
        return 'tweet'


tweetsXtags = Table('tweetsXtags', Base.metadata,
                    Column('tweetID', Integer), # ForeignKey('tweets.tweetID')),
                    Column('tagID', Integer), # ForeignKey('hashtags.tagID'))
                    )

##################### Non definitional stuff

class Tweet(Tweets):
    """Better named alias"""
    def __init__(self, **kwargs):
        super().__init__( **kwargs)


def _make_defined_data(data, defined_keys):
    """Takes the incoming tweet data and pulls out
    all of the items which go into fields of the
    db and puts the rest into a json string under other_data
    """
    # This will be the data that goes directly into the model
    defined_data = {}
    # This will be the data that goes into the other_data field
    forJson = { }

    for k in data.keys():
        datum = data[k]
        # check whether it is a dict and encode, if necessary
        if type(datum) == dict:
            datum = json.dumps(datum)

        if k in defined_keys:
            defined_data[k] = datum

        else:
            forJson[k] = datum

    # Set the data that didn't have a field
    # to the json field
    defined_data['other_data'] = json.dumps(forJson)

    return defined_data


def TweetFactory( data: dict ):
    """This consumes a dictionary of data and returns a
    Tweet object. If the dictionary contains keys which do not
    correspond to a field in User, such fields are added to the json
    column `other_data`
    This is necessary because Twitter sometimes updates the keys in the results
    that we receive and sqlalchemy will be sad if pass in data which lacks
    defined fields.
    NB, this simply creates and populates the Tweet object. It does not add or
    commit it to the database
    :type data: dict
    """
    # The first step is to sort the incoming data
    mapper = inspect(Tweets)

    # create the list of valid keys
    defined_keys = [column.key for column in mapper.attrs]

    defined_data = _make_defined_data(data, defined_keys)

    # Now set any fields which do not have couterparts in the
    # the incoming data
    defined_data['tweetID'] = int(data['id_str'])
    defined_data['userID'] = int(data['user']['id_str'])
    defined_data['tweetText'] = data['text'].encode('unicode_escape')

    # create a new instance with the data
    return Tweet(**defined_data)


class User(Users):
    """Better named alias"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def UserFactory( data: dict ):
    """This consumes a dictionary of data and returns a
    User object. If the dictionary contains keys which do not
    correspond to a field in User, such fields are added to the json
    column `other_data`
    This is necessary because Twitter sometimes updates the keys in the results
    that we receive and sqlalchemy will be sad if pass in data which lacks
    defined fields.
    NB, this simply creates and populates the User object. It does not add or
    commit it to the database
    :type data: dict
    """
    # The first step is to sort the incoming data
    mapper = inspect(Users)
    # These will be the fields to save to corresponding columns
    # in the database
    defined_keys = [column.key for column in mapper.attrs]

    defined_data = _make_defined_data(data, defined_keys)

    # Now set any fields which do not have couterparts in the
    # the incoming data
    defined_data['userID'] = int(defined_data['id'])

    # create a user instance with the data
    return User(**defined_data)

    #
    # # This will be the data that goes directly into the model
    # defined_data = {}
    # # This will be the data that goes into the other_data field
    # forJson = { }
    #
    # for k in data.keys():
    #     datum = data[k]
    #     # check whether it is a dict and encode, if necessary
    #     if type(datum) == dict:
    #         datum = json.dumps(datum)
    #
    #     if k in defined_keys:
    #         defined_data[k] = datum
    #
    #     else:
    #         forJson[k] = datum


def create_db_tables(engine, seed=False):
    """Creates tables in the database
    Create all tables in the engine.
    This is equivalent to "Create Table" statements in raw SQL.
    # """
    # engine = DatabaseAccessObjects.EngineMakers.initialize_engine()
    # create the tables
    Base.metadata.create_all(engine)
    # metadata = MetaData( )
