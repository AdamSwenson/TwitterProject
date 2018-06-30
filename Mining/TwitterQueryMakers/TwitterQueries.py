"""
Created by adam on 6/28/18
"""
__author__ = 'adam'

def make_query(terms):
    """
    >>>terms =['pain', 'fibromyalgia', 'migraine']
    >>>assert make_query(terms) == "l=en&q=pain%2C OR fibromyalgia%2C OR migraine"
    :return:
    """
    seperator = '%2C OR '
    stem = "q="
    last = terms[-1:][0]

    for term in terms:
        stem += "%s" % term
        if term != last:
            stem+= seperator
    return stem



class TweetsGetter:

    def __init__(self, connection):
        self.conn = connection.connection

    def get_tweets_for_search_terms( self, search_terms, beforeId=None, afterId=None ):
        """
        Returns tweet objects for the given user
        :param userId:
        :param beforeId:
        :param afterId:
        :return: list
        """
        query = make_query(search_terms)

        results = self.conn.GetSearch(raw_query=query, max_id=beforeId, since_id=afterId)
        return [r._json for r in results]

if __name__ == '__main__':
    pass