"""
Created by adam on 11/11/15
Formerly in TextProcessingTools
"""
__author__ = 'adam'

from TextProcessingTools.TextProcessors.ClassificationTools import *

from TextProcessingTools.TextTools.Processors.Parents import IProcessor


class WordBagMaker(IProcessor):
    """
    General class for taking something with strings and processing the text for bag of words type analyses.

    Before running the run command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of IFilter objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
    """

    def __init__(self):
        super().__init__()
        self._ignore = ()
        self.masterbag = []

    def add_to_ignorelist(self, list_to_ignore):
        """
        Add a list of strings to the internally held tuple of strings to ignore in processing text
        Example:
            bagmaker = WordBagMaker()
            bagmaker.add_to_ignorelist(ignore.get_list())
            bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
            bagmaker.add_to_ignorelist(list(string.punctuation))

        Args:
            list_to_ignore: List of strings to ignore.
        """
        self._ignore = list(self._ignore)
        [self._ignore.append(i) for i in list_to_ignore]
        self._ignore = set(self._ignore)
        self._ignore = tuple(self._ignore)

    def process(self, to_process):
        """
        Processes list of strings into a word bag stored in self.masterbag

        Args:
            to_process: List of strings to run
        """
        assert(isinstance(to_process, list))
        for t in to_process:
            # run text
            words = self._make_wordbag(t)
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            self.masterbag += words

    def _make_wordbag(self, text):
        """
        Takes a bunch of sentences and extracts all the words, makes them lowercase, and returns them in a list

        Args:
            text: String text to be word tokenized

        Returns:
            List of words, all lower case
        """
        return [word.lower() for sent in nltk.tokenize.sent_tokenize(text) for word in nltk.tokenize.word_tokenize(sent)]

    def _check_unwanted(self, word):
        """
        Args:
            word: String to evaluate with IFilter objects in _cleaners
        Returns:
            False if the the string is to be left out
            True if the string is to be included
        """
        for cleaner in self._cleaners:
            if cleaner.clean(word) is False:
                return False
        return True


class TweetTextWordBagMaker(WordBagMaker):
    """
    This takes a list of dictionaries containing tweetID and tweetText and processes the texts for bag of words type analyses.

    Before running the run command, all lists of strings to ignore should be loaded using add_to_ignorelist()

    Attributes:
        _cleaners: List of IFilter objects
        masterbag: List containing all words
        _ignore: Tuple of strings to ignore while filtering
        tweet_tuples: List containing tuples with the structure (tweetID, [list of words in tweet])
    """
    def __init__(self):
        self.tweet_tuples = []
        WordBagMaker.__init__(self)

    def process(self, to_process):
        """
        Args:
            to_process: List of tweet dictionary objects with keys 'tweetID' and 'tweetText'

        Best time 225.85651803

        Example
        bagmaker = TweetTextWordBagMaker()
        bagmaker.add_to_ignorelist(ignore.get_list())
        bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
        """
        for t in to_process:
            tweetid = t['tweetID']
            # run text
            words = self._make_wordbag(t['tweetText'])
            words = [w for w in words if self._check_unwanted(w) and w not in self._ignore]
            # run tuple
            tweet_tuple = (tweetid, words)
            self.tweet_tuples.append(tweet_tuple)
            self.masterbag += words

