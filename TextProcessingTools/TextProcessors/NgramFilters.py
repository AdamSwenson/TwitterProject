"""
Created by adam on 11/8/16
"""
__author__ = 'adam'


import nltk
# from nltk.corpus import wordnet as wn


class INgramFilter(object):
    """
    Interface for filters on ngrams
    """

    def __init__(self, **kwargs):
        pass

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        Returns:
            The collocation_finder after has been filtered
        """
        raise NotImplementedError


###################################
# INgramFilter implementations    #
###################################

class CustomFilter(INgramFilter):
    """
    Wrapper for applying arbitrary filter to the collocation finder
    e.g., for getting where 'and' is at trigram[1] but not beginning or end: lambda w1, w2, w3: 'and' in (w1, w3)
    """

    def __init__(self):
        self.filter_function = lambda x: x
        INgramFilter.__init__(self)

    def set_filter(self, filter_function):
        self.filter_function = filter_function

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        """
        assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
        return collocation_finder.apply_ngram_filter(self.filter_function)


class WordFilter(INgramFilter):
    """
    Wrapper for filtering by specific strings
    Make sure to set filter_words before calling filter

    Attributes:
        _filter_words: Tuple holding words to filter by, can be set with string, tuple, or list
    """

    def __init__(self):
        self._filter_words = ()
        INgramFilter.__init__(self)

    @property
    def filter_words(self):
        return self._filter_words

    @filter_words.setter
    def filter_words(self, words):
        """
        adds words to the internally held tuple of filter_words
        Arguments:
            :param words: Tuple, list, or individual word to add to the filter words
        """
        self._filter_words = list(self._filter_words)
        if isinstance(words, list):
            self._filter_words += words
        elif isinstance(words, str):
            self._filter_words.append(words)
        elif isinstance(words, tuple):
            self._filter_words += list(words)
        self._filter_words = tuple(self._filter_words)

    def filter(self, collocation_finder):
        """
        Arguments:
            collocation_finder: Instance of nltk.collocations.AbstractCollocationFinder
        """
        assert isinstance(collocation_finder, nltk.collocations.AbstractCollocationFinder)
        return collocation_finder.apply_word_filter(lambda w: w in self.filter_words)