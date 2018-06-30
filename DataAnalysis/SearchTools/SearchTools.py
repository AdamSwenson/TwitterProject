"""
Created by adam on 11/8/16
"""
__author__ = 'adam'

import pandas as pd

import environment as env
import Models.TweetORM as TweetORM

pd.options.display.max_rows = 999  # let pandas dataframe listings go long

def isRetweet(text):
    """
    Classifies whether a tweet is a retweet based on how it starts
    """
    if text[:4] == "RT @":
        return True
    if text[:4] == "MT @":
        return True
    return False


def isReply(tweetObject):
    if tweetObject.in_reply_to_screen_name != None:
        return True
    if tweetObject.text[0] == '@':
        return True
    return False


search_terms = ['Spoonie',
                'CRPS',
                'Migraine',
                'RSD',
                'Fibro',
                'Fibromyalgia',
                'Vulvodynia',
                'ChronicPain',
                'pain',
                'endometriosis',
                'neuropathy',
                'arthritis',
                'neuralgia']


class Condition(object):
    """
    Data holder
    """

    def __init__(self, name, filepath=env.DATA_FOLDER):
        self.name = name
        self.datafile = "%s/%s.csv" % (filepath, self.name)
        self.indexer_ids = set([])
        self.userids = set([])
        self.users = ''

    def get_total(self):
        """
        Returns the total number of users
        """
        return len(self.userids)

    def get_maxid(self):
        """
        Returns the highest indexerid
        """
        return max(list(self.indexer_ids))

    def add_userid(self, userid):
        """
        Add userid to list
        """
        self.userids.update([userid])

    def add_indexer_id(self, indexer_id):
        """
        Add indexerid
        """
        self.indexer_ids.update([indexer_id])


class UserGetter(object):
    """
    Retrieves user info and builds dataframe of users when given list of ids
    """

    def __init__(self, sql_alchemy_engine):
        self.engine = sql_alchemy_engine

    def _get_user(self, searchterm, userid):
        query = "SELECT userID, indexer, '%s' AS term, description AS profile FROM users WHERE userid = %s" % (
            searchterm, userid)
        return pd.read_sql_query(query, self.engine)

    def get_from_list(self, searchterm, userids):
        """
        Args:
            searchterm: String that was searched for
            userids: List of userids to retrieve
        Returns:
            Dataframe with labels userID, indexer, term, profile
        """
        frames = []
        for uid in userids:
            frames.append(self._get_user(searchterm, uid))
        return pd.concat(frames)

    def get_from_condition_object(self, condition_object):
        """
        Reads userids etc from a Condition object and stores users in the object
        """
        assert (isinstance(condition_object, Condition))
        result = self.get_from_list(condition_object.name, condition_object.userids)
        condition_object.users = result
        return condition_object
