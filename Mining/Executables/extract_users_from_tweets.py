"""
Created by adam on 8/16/18
"""
__author__ = 'adam'

%cd twitterproject
import sys
sys.argv = ['data-analysis']
import environment

import pandas as pd
import numpy as np

#Plotting
%matplotlib inline
from matplotlib import pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")

from TwitterDatabase.Repositories import DataRepositories as DR
from TwitterDatabase.DatabaseAccessObjects import DataConnections as DC
from TwitterDatabase.Models.WordORM import Word
from TwitterDatabase.Models.TweetORM import Users as User
from TwitterDatabase.Models.TweetORM import Tweet
from TwitterDatabase.Models.TweetORM import UserFactory

from Server.ServerTools import Helpers

from sqlalchemy.orm import sessionmaker

dao = DC.MySqlConnection(environment.CREDENTIAL_FILE)
Session = sessionmaker(bind=dao.engine)


USER_FIELDS_TO_UPDATE = ('friends_count', 'followers_count', 'statuses_count' )

def extract_user_dict_from_tweet(tweet: Tweet):
    """Takes the other_data field from a tweet object and
    extracts the data for the user from it.
    It returns a dictionary rather than a User model object
    because we might want to try looking up whether the user
    exists before creating a new user object.

    :type tweet Tweet
    :returns dict
    """
    if tweet.other_data and len(tweet.other_data) > 0:
        # extract the json
        j = json.loads(tweet.other_data)
        # extract the user json from the created dict
        u = json.loads(j['user'])
        return u


# Test
tweet = Tweet()
# check where no other data
assert(isinstance(extract_user_dict_from_tweet(tweet), type(None)))
# check happy path
tweet.other_data = "{\"id\": 1013218630740238336, \"id_str\": \"1013218630740238336\", \"text\": \"Works for me.. Was a pain in the ass anyways waiting the extra time for the prescription to be filled to find out i\\u2026 https://t.co/XNW11OrC0p\", \"truncated\": true, \"entities\": \"{\\\"hashtags\\\": [], \\\"symbols\\\": [], \\\"user_mentions\\\": [], \\\"urls\\\": [{\\\"url\\\": \\\"https://t.co/XNW11OrC0p\\\", \\\"expanded_url\\\": \\\"https://twitter.com/i/web/status/1013218630740238336\\\", \\\"display_url\\\": \\\"twitter.com/i/web/status/1\\\\u2026\\\", \\\"indices\\\": [117, 140]}]}\", \"metadata\": \"{\\\"iso_language_code\\\": \\\"en\\\", \\\"result_type\\\": \\\"recent\\\"}\", \"in_reply_to_status_id\": null, \"in_reply_to_status_id_str\": null, \"in_reply_to_user_id\": null, \"in_reply_to_user_id_str\": null, \"user\": \"{\\\"id\\\": 48058862, \\\"id_str\\\": \\\"48058862\\\", \\\"name\\\": \\\"Teresa\\\", \\\"screen_name\\\": \\\"RessyM\\\", \\\"location\\\": \\\"Toronto, Ontario\\\", \\\"description\\\": \\\"WoW Addon Maintainer (ARL & Collectinator), Curse/Twitch: RessyM\\\\nBlizzard Tech Support MVP\\\", \\\"url\\\": null, \\\"entities\\\": {\\\"description\\\": {\\\"urls\\\": []}}, \\\"protected\\\": false, \\\"followers_count\\\": 1033, \\\"friends_count\\\": 475, \\\"listed_count\\\": 40, \\\"created_at\\\": \\\"Wed Jun 17 18:24:23 +0000 2009\\\", \\\"favourites_count\\\": 15340, \\\"utc_offset\\\": null, \\\"time_zone\\\": null, \\\"geo_enabled\\\": false, \\\"verified\\\": false, \\\"statuses_count\\\": 57156, \\\"lang\\\": \\\"en\\\", \\\"contributors_enabled\\\": false, \\\"is_translator\\\": false, \\\"is_translation_enabled\\\": false, \\\"profile_background_color\\\": \\\"1A1B1F\\\", \\\"profile_background_image_url\\\": \\\"http://abs.twimg.com/images/themes/theme9/bg.gif\\\", \\\"profile_background_image_url_https\\\": \\\"https://abs.twimg.com/images/themes/theme9/bg.gif\\\", \\\"profile_background_tile\\\": false, \\\"profile_image_url\\\": \\\"http://pbs.twimg.com/profile_images/801860512220901377/5qw96jgB_normal.jpg\\\", \\\"profile_image_url_https\\\": \\\"https://pbs.twimg.com/profile_images/801860512220901377/5qw96jgB_normal.jpg\\\", \\\"profile_banner_url\\\": \\\"https://pbs.twimg.com/profile_banners/48058862/1479691314\\\", \\\"profile_link_color\\\": \\\"2FC2EF\\\", \\\"profile_sidebar_border_color\\\": \\\"181A1E\\\", \\\"profile_sidebar_fill_color\\\": \\\"252429\\\", \\\"profile_text_color\\\": \\\"666666\\\", \\\"profile_use_background_image\\\": true, \\\"has_extended_profile\\\": true, \\\"default_profile\\\": false, \\\"default_profile_image\\\": false, \\\"following\\\": false, \\\"follow_request_sent\\\": false, \\\"notifications\\\": false, \\\"translator_type\\\": \\\"none\\\"}\", \"geo\": null, \"coordinates\": null, \"place\": null, \"contributors\": null, \"is_quote_status\": false, \"possibly_sensitive\": false}"
assert(extract_user_dict_from_tweet(tweet)['id'] == 48058862)

def get_user_by_id(user_id, session):
    u = session.query(User).filter(User.userID == user_id).first()
    return u


def update_or_create_user_from_tweet(tweet: Tweet, session):
    """Extracts the user data from the tweet's other_data json field
    and saves a user object. If there already is a user with that id, it
    updates their properties. Otherwise, it creates a new user object
    :type tweet: Tweet
    :returns User
    """

    data = extract_user_dict_from_tweet(tweet)

    if data is not None:

        # Try to load existing user
        userId = tweet.userID
        user = get_user_by_id(userId, session)

        if user is None:
            # make user from the json
            user = UserFactory(data)
            user.audit_data = {'created_from_tweet' : tweet.tweetID}
        else:
            # make a copy, we need to be a bit sneaky because sqlalchemy isn't watching the json field
            # but it will freak out over a Detached Instance
            j = {k : user.audit_data[k] for k in user.audit_data.keys()}
            # update relevant fields
            audit =  { 'event': 'update_from_tweet', 'tweetId' : tweet.tweetID}
            for f in USER_FIELDS_TO_UPDATE:
                setattr(user, f, data[f])
                audit[f] = data[f]
            j[tweet.tweetID] = audit
            user.audit_data = j

            # return the object in case needed
        return user


session = Session()

users = 0
FLUSH_LIMIT = 10


for tweet in session.query(Tweet).filter(Tweet.other_data.isnot(None)):
    user = update_or_create_user_from_tweet(tweet, session)

    users += 1

    if(users % FLUSH_LIMIT == 0):
        print('flushing at %s users' % users)
        session.commit()

print("%s users created or updated" % users)
session.commit()
session.close()



for tweet in session.query(Tweet).limit(10):
    print(tweet.tweetID)

session.close()




# Testing updates

session = Session()

u = session.query(User).filter(User.screen_name == 'Adam').first()

assert(u is not None)

u.add_tweet_update_info_to_audit_data({'jip': 'j'})

j = {k : u.audit_data[k] for k in u.audit_data.keys()}

if __name__ == '__main__':
    pass