"""
Created by adam on 8/16/18
"""
__author__ = 'adam'

from sqlalchemy.orm import sessionmaker
import environment

from TwitterDatabase.DatabaseAccessObjects import DataConnections as DC
from TwitterDatabase.Models.WordORM import Word
from TwitterDatabase.Models.TweetORM import Users as User
from TwitterDatabase.Models.TweetORM import Tweet
from TwitterDatabase.Models.TweetORM import UserFactory

from Mining.SearchResultsProcessing import UserExtractionTools as UET

dao = DC.MySqlConnection(environment.CREDENTIAL_FILE)
Session = sessionmaker(bind=dao.engine)


if __name__ == '__main__':
    FLUSH_LIMIT = 100
    session = Session()
    UET.harvest_users_from_tweets(session, FLUSH_LIMIT)
