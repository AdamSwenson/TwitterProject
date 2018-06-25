"""
Created by adam on 11/18/15
"""
__author__ = 'adam'

import unittest
from TextTools.TextProcessors.WordBagMakers import *


# class WordBagMakerTest(unittest.TestCase):
#
#     def setUp(self):
#         self.object = WordBagMaker()
#
#     def test_add_to_ignore_list(self):
#         # prep
#         test = ['dog', 'fish', 93, 'fish']
#         # call
#         self.object.add_to_ignorelist(test)
#         # check
#         self.assertEqual(type(self.object._ignore) is tuple, 'converts back to tuple')
#         self.assertEqual(len(set(test)), len(self.object._ignore, 'only one token per type'))
#         self.assertEqual(tuple(set(test)), self.object._ignore, 'contents as expected')


class LemmatizerTest(unittest.TestCase):
    """
    Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
    """
    def setUp(self):
        self.object = Lemmatizer()

    def test_process(self):
        self.assertIsInstance(self.object.lemmatizer, nltk.stem.WordNetLemmatizer)

    def test_process_excepts_if_not_string(self):
        self.assertRaises( AssertionError, self.object.run( 4 ) )


class PorterStemmerTest(unittest.TestCase):
    def setUp(self):
        self.object = PorterStemmer()

    def test_process(self):
        self.assertIsInstance(self.object.stemmer, nltk.stem.PorterStemmer)

    def test_process_excepts_if_not_string(self):
        self.assertRaises( AssertionError, self.object.run( 4 ) )


class WordBagMakerTest(unittest.TestCase):
    def setUp(self):
        self.object = WordBagMaker()

    def tearDown(self):
        self.object = ''

    def test_add_to_ignorelist(self):
        """
        The tested function combines the lists, removes duplicates, and converts to a tuple
        """
        testlist1 = [1, 2]
        testlist2 = [2, 3, 4, 5]
        expect = (1, 2, 3, 4, 5)

        self.object.add_to_ignorelist(testlist1)
        # make sure adds to the list
        # t1 = list(self.object.ignore).sort()
        # self.assertListEqual(t1, testlist1.sort())
        self.object.add_to_ignorelist(testlist2)
        # make sure edited out the duplicates
        self.assertTupleEqual(self.object._ignore, expect)

    def test__make_wordbag(self):
        test = "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"
        expect = ["the", "quick", "brown", "fox", "became", "a", "delicious", "taco", "for", "the", "hungry", "cat", ".", "all", "lived", "happily", "ever", "after"]
        result = self.object._make_wordbag(test)
        self.assertListEqual(result, expect)

    @unittest.skip
    def test_process(self):
        test = ["The first tweet.",  "It has text", "The quick brown fox became a delicious taco for the hungry cat.",
                "All lived happily ever after"]
        expect = ["first", "tweet", "text", "quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat",
                  "lived", "happily", "ever"]
        self.object.add_to_ignorelist([".", ","])
        self.object.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        self.object.process(test)
        self.assertEqual(self.object.masterbag, expect)


class TweetTextWordBagMakerTest(unittest.TestCase):
    def setUp(self):
        self.object = TweetTextWordBagMaker()

    def tearDown(self):
        self.object = ''

    def test_add_to_ignorelist(self):
        """
        The tested function combines the lists, removes duplicates, and converts to a tuple
        """
        testlist1 = [1, 2]
        testlist2 = [2, 3, 4, 5]
        expect = (1, 2, 3, 4, 5)

        self.object.add_to_ignorelist(testlist1)
        # make sure adds to the list
        # t1 = list(self.object.ignore).sort()
        # self.assertListEqual(t1, testlist1.sort())
        self.object.add_to_ignorelist(testlist2)
        # make sure edited out the duplicates
        self.assertTupleEqual(self.object._ignore, expect)

    def test__make_wordbag(self):
        test = "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"
        expect = ["the", "quick",  "brown", "fox", "became", "a", "delicious", "taco", "for", "the", "hungry", "cat", ".", "all", "lived", "happily", "ever", "after"]
        result = self.object._make_wordbag(test)
        self.assertListEqual(result, expect)

    # def test__filter_ignored_terms(self):
    #     to_remove = ['dog', 'cow']
    #     test = ['cat', 'dog', 'fish', 'cow']
    #     expect = ['cat', 'fish']
    #     self.object.add_to_ignorelist(to_remove)
    #     result = self.object._filter_ignored_terms(test)
    #     self.assertListEqual(result, expect)

    # def test__filter_usernames(self):
    #     test = ['taco', '@burrito', 'cat', '@dog']
    #     expect = ['taco', 'cat']
    #     result = self.object._filter_usernames(test)
    #     self.assertListEqual(result, expect)

    # def test__filter_urls(self):
    #     test = ['taco', '//t.co', 'cat', '//t.co']
    #     expect = ['taco', 'cat']
    #     result = self.object._filter_urls(test)
    #     self.assertListEqual(result, expect)

    @unittest.skip
    def test_process(self):
        test = [{'tweetID': 1, 'tweetText': "The first tweet. It has text"},
                {'tweetID': 2, 'tweetText': "The quick brown fox became a delicious taco for the hungry cat. All lived happily ever after"}]
        expect = ["first", "tweet", "text", "quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat",
                  "lived", "happily", "ever"]
        self.object.add_to_ignorelist([".", ","])
        self.object.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        self.object.process(test)
        self.assertEqual(self.object.masterbag, expect)
        self.assertTupleEqual(self.object.tweet_tuples[0], (1, ["first", "tweet", "text"]))
        self.assertTupleEqual(self.object.tweet_tuples[1], (2, ["quick", "brown", "fox", "became", "delicious", "taco", "hungry", "cat", "lived", "happily", "ever"]))

