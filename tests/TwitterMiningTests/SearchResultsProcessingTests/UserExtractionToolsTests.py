import unittest

from SearchResultsProcessing.UserExtractionTools import *


class extract_user_dict_from_tweetTest( unittest.TestCase ):

    def test_returns_none_when_no_other_data( self ):
        # Test
        tweet = Tweet()
        # check where no other data
        self.assertIsNone(extract_user_dict_from_tweet(tweet))

    def test_creates_dict_from_tweet_other_data( self ):
            # Test
            tweet = Tweet()
            # check happy path
            tweet.other_data = "{\"id\": 1013218630740238336, \"id_str\": \"1013218630740238336\", \"text\": \"Works for me.. Was a pain in the ass anyways waiting the extra time for the prescription to be filled to find out i\\u2026 https://t.co/XNW11OrC0p\", \"truncated\": true, \"entities\": \"{\\\"hashtags\\\": [], \\\"symbols\\\": [], \\\"user_mentions\\\": [], \\\"urls\\\": [{\\\"url\\\": \\\"https://t.co/XNW11OrC0p\\\", \\\"expanded_url\\\": \\\"https://twitter.com/i/web/status/1013218630740238336\\\", \\\"display_url\\\": \\\"twitter.com/i/web/status/1\\\\u2026\\\", \\\"indices\\\": [117, 140]}]}\", \"metadata\": \"{\\\"iso_language_code\\\": \\\"en\\\", \\\"result_type\\\": \\\"recent\\\"}\", \"in_reply_to_status_id\": null, \"in_reply_to_status_id_str\": null, \"in_reply_to_user_id\": null, \"in_reply_to_user_id_str\": null, \"user\": \"{\\\"id\\\": 48058862, \\\"id_str\\\": \\\"48058862\\\", \\\"name\\\": \\\"Teresa\\\", \\\"screen_name\\\": \\\"RessyM\\\", \\\"location\\\": \\\"Toronto, Ontario\\\", \\\"description\\\": \\\"WoW Addon Maintainer (ARL & Collectinator), Curse/Twitch: RessyM\\\\nBlizzard Tech Support MVP\\\", \\\"url\\\": null, \\\"entities\\\": {\\\"description\\\": {\\\"urls\\\": []}}, \\\"protected\\\": false, \\\"followers_count\\\": 1033, \\\"friends_count\\\": 475, \\\"listed_count\\\": 40, \\\"created_at\\\": \\\"Wed Jun 17 18:24:23 +0000 2009\\\", \\\"favourites_count\\\": 15340, \\\"utc_offset\\\": null, \\\"time_zone\\\": null, \\\"geo_enabled\\\": false, \\\"verified\\\": false, \\\"statuses_count\\\": 57156, \\\"lang\\\": \\\"en\\\", \\\"contributors_enabled\\\": false, \\\"is_translator\\\": false, \\\"is_translation_enabled\\\": false, \\\"profile_background_color\\\": \\\"1A1B1F\\\", \\\"profile_background_image_url\\\": \\\"http://abs.twimg.com/images/themes/theme9/bg.gif\\\", \\\"profile_background_image_url_https\\\": \\\"https://abs.twimg.com/images/themes/theme9/bg.gif\\\", \\\"profile_background_tile\\\": false, \\\"profile_image_url\\\": \\\"http://pbs.twimg.com/profile_images/801860512220901377/5qw96jgB_normal.jpg\\\", \\\"profile_image_url_https\\\": \\\"https://pbs.twimg.com/profile_images/801860512220901377/5qw96jgB_normal.jpg\\\", \\\"profile_banner_url\\\": \\\"https://pbs.twimg.com/profile_banners/48058862/1479691314\\\", \\\"profile_link_color\\\": \\\"2FC2EF\\\", \\\"profile_sidebar_border_color\\\": \\\"181A1E\\\", \\\"profile_sidebar_fill_color\\\": \\\"252429\\\", \\\"profile_text_color\\\": \\\"666666\\\", \\\"profile_use_background_image\\\": true, \\\"has_extended_profile\\\": true, \\\"default_profile\\\": false, \\\"default_profile_image\\\": false, \\\"following\\\": false, \\\"follow_request_sent\\\": false, \\\"notifications\\\": false, \\\"translator_type\\\": \\\"none\\\"}\", \"geo\": null, \"coordinates\": null, \"place\": null, \"contributors\": null, \"is_quote_status\": false, \"possibly_sensitive\": false}"
            self.assertEqual(extract_user_dict_from_tweet(tweet)['id'], 48058862)




if __name__ == '__main__':
    unittest.main()
