"""
Tools for downloading a user's info or their tweets
Created by adam on 6/21/18

https://developer.twitter.com/en/docs/accounts-and-users/follow-search-get-users/api-reference/get-users-lookup

"""
from Server.ServerTools.Helpers import convert_object_into_dict

__author__ = 'adam'


def make_query(connection, query, limit, **kwargs):
    try:
        return connection.search.tweets(q=query, count=limit)
    except Exception as e:
        raise e


def make_query_to_get_users_profiles(userIds):
    """Returns a query to retrieve the profile for the indicated list of
    user ids
    Api info:
        parameter name: user_id
        values: A comma separated list of user IDs, up to 100 are allowed in a single request.
        Notes: You are strongly encouraged to use a POST for larger requests.
    """
    q = "user_id="

    for uid in userIds:
        q += "%s," % uid

    # the above left a comma at the very end,
    # so we return all but the last character
    return q[:-1]



class UsersGetter:

    def __init__(self, connection):
        self.conn = connection.connection
    
    def get_profiles_for_users( self, userIds ):
        # query = make_query_to_get_users_profiles(userIds)
        # print("query", query)
        return self.conn.UsersLookup( user_id=userIds, return_json=True )

    def get_tweets_for_user( self, userId, beforeId=None, afterId=None ):
        """
        Returns tweet objects for the given user
        :param userId:
        :param beforeId:
        :param afterId:
        :return: list
        """
        results = self.conn.GetUserTimeline(userId, max_id=beforeId, since_id=afterId)
        return [r._json for r in results]



if __name__ == '__main__':
    pass



