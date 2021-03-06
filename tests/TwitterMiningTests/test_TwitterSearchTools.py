from Loggers.SearchLoggers import SearchLogger
from Mining.Miner.TwitterSearchTools import *
from tests.helpers.DaoMocks import *
from tests.helpers.TwitterMocks import *
from tests.helpers.ObserverMocks import *

# CREDENTIALS_FILE = ''
import unittest


class SearchTest(unittest.TestCase):
    def setUp(self):
        self.object = Search()
        self.redis = RedisDaoMock()
        self.couch = CouchDaoMock()
        self.logger = SearchLogger()
        self.observer = ISearchObserverMock()

    def tearDown(self):
        self.object = ''
        self.redis = ''
        self.couch = ''
        self.observer = ''

    def test_attach_observer(self):
        self.object.attach_observer(self.observer)
        self.assertTrue(len(self.object._observers), 1)

    def test_detach_observer(self):
        # TODO check with multiple observers that correct one removed
        self.object._observers.append(self.observer)
        self.assertEqual(len(self.object._observers), 1)
        self.object.detach_observer(self.observer)
        self.assertEqual(len(self.object._observers), 0)

    def test_detach_observer_exception(self):
        self.object._observers.append({'kind': 'housecat'})
        with self.assertRaises(ObserverError):
            self.object.detach_observer(self.observer)

    def test_notify_observers(self):
        # TODO try with multiple observers
        # setup
        self.object._observers.append(self.observer)
        self.assertFalse(self.observer.update_called)
        # test
        self.object.notify_observers()
        self.assertTrue(self.observer.update_called)
        self.assertEqual(self.observer.caller, self.object)

    def test_set_redis_service(self):
        self.object.set_redis_service(self.redis)
        self.assertEqual(self.object.redis, self.redis)

    def test_set_couch_service(self):
        self.object.set_couch_service(self.couch)
        self.assertEqual(self.object.couch, self.couch)

    def test_set_logger(self):
        self.object.set_logger(self.logger)
        self.assertEqual(self.object.logger, self.logger)

    def test_set_twitter_connection(self):
        self.object.set_twitter_connection('credentials/filepath')
        self.assertIsInstance(self.object.twitter_conn, TwitterMock)

    def test__get_oldest_tweet(self):
        tweetid = 123456789
        self.redis.set_response(tweetid)
        self.object.set_redis_service(self.redis)
        result = self.object._get_oldest_tweet()
        self.assertEqual(result, tweetid)

    def test__get_newest_tweet(self):
        tweetid = 123456789
        self.redis.set_response(tweetid)
        self.object.set_redis_service(self.redis)
        result = self.object._get_newest_tweet()
        self.assertEqual(result, tweetid)

    def test__get_starting_tweet(self):
        tweetid = 123456789
        self.redis.set_response(tweetid)
        self.object.set_redis_service(self.redis)
        result = self.object._get_starting_tweet(True)
        self.assertEqual(result, tweetid)
        # false case
        tweetid2 = 1234566543
        self.redis.set_response(tweetid2)
        self.object.set_redis_service(self.redis)
        result = self.object._get_starting_tweet(False)
        self.assertEqual(result, tweetid2)
        # Null recent case
        tweetid = 123456789
        self.redis.set_response(tweetid)
        self.object.set_redis_service(self.redis)
        result = self.object._get_starting_tweet('')
        self.assertEqual(result, None)

    def test__handle_id_field(self):
        bad = 12234
        good = 1234567
        tweet = {'id_str': good, '_id': bad}
        result = self.object._handle_id_field(tweet)
        self.assertEqual(result, {'id_str': good, '_id': good})

    def test__search_twitter(self):
        tag = 'testtag'
        limittweet = 987665
        self.object.set_twitter_connection(login)
        self.object.limitTweet = limittweet
        result = self.object._search_twitter(tag, True)
        self.assertEqual(result[0], {'word_map_table_creation_query': tag, 'count': 100, 'since_id': limittweet, 'max_id': None})
        result = self.object._search_twitter(tag, False)
        self.assertEqual(result[0], {'word_map_table_creation_query': tag, 'count': 100, 'since_id': None, 'max_id': limittweet})

    def test__process_search_results(self):
        bad = 12234
        good = 1234567
        tweet1 = {'id_str': good, '_id': bad}
        tweet2 = {'id_str': good, '_id': bad}
        goodtweet = {'id_str': good, '_id': good}
        search_results = {'crap': ['sltuff'], 'statuses': [tweet1, tweet2]}
        result = self.object._process_search_results(search_results)
        self.assertEqual(result, [goodtweet, goodtweet])

    # def test__process_search_results_exception(self):
    #     search_results = {'taco': 78}
    #     with self.assertRaises(SearchError):
    #         self.object._process_search_results(search_results)

if __name__ == '__main__':
    unittest.main()