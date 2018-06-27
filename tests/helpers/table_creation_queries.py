"""
Created by adam on 6/27/18
"""
__author__ = 'adam'

make_hashtags_table = """
  CREATE TABLE hashtags (
        tagID INTEGER PRIMARY KEY AUTOINCREMENT,
        hashtag TEXT unique)
        """

make_tweets_table = """
    CREATE TABLE `tweets` (
        `tweetID` INTEGER PRIMARY KEY,
        `userID` TEXT,
        `tweetText` TEXT,
        `favorite_count` TEXT,
        `source` TEXT,
        `retweeted` TEXT,
        `in_reply_to_screen_name` TEXT,
        `retweet_count` TEXT,
        `favorited` TEXT,
        `lang` TEXT,
        `created_at` TEXT,
        `updated` TEXT,
        `profile_background_tile` TEXT)
        """

make_users_table = """
    CREATE TABLE `users` (
        `userID` INTEGER PRIMARY KEY,
        `lang` TEXT,
        `utc_offset` TEXT,
        `verified` TEXT,
        `description` TEXT,
        `friends_count` TEXT,
        `url` TEXT,
        `time_zone` TEXT,
        `created_at` TEXT,
        `name` TEXT,
        `entities` TEXT,
        `followers_count` TEXT,
        `screen_name` TEXT,
        `id_str` TEXT,
        `favourites_count` TEXT,
        `statuses_count` TEXT,
        `id` TEXT,
        `location` TEXT,
        `is_translation_enabled` TEXT)
        """

make_tweetsxtags_table = """
    CREATE TABLE `tweetsXtags` (
        `tweetID`TEXT,
        `tagID` TEXT)
        """
