"""
This contains text modification tools which
receive a string and return a boolean for whether
that string should be included in the resulting data

Created by adam on 11/8/16
"""
__author__ = 'adam'

import dawg
import re
import string
from nltk.corpus import stopwords
english_stops = set(stopwords.words('english'))

from TextProcessingTools.TextTools.Processors.Exceptions import ExcludedString


class IFilter(object):
    """
    Interface for text processing objects which take a word as input and
    return True or False to indicate whether the string should be
    included in the resulting data

    These are normally placed in a queue and then ran in sequence as part
    of a list comprehension. Objects like TweetTextWordBagMaker receive
    a list of these objects
    """

    def run(self, word, **kwargs):
        """Runs the operation on the string. This is the main method"""
        raise NotImplementedError


#####################################
# IFilter implementations          #
#####################################

class IgnoreListFilter(IFilter):
    """
        Detects whether the string is in the ignore list and returns
        a boolean so it can be removed.
        TODO: Make this better
        """
    __name__ = 'IgnoreListFilter'

    def __init__(self):
        super().__init__()
        self._ignore = ()

    def run(self, word, **kwargs):
        if word in self._ignore:
            raise ExcludedString
            return False
        else:
            return True

    def add_to_ignorelist(self, to_ignore):
        """
        Add a list of strings to the internally held tuple of strings to ignore in processing text
        Example:
            bagmaker = WordBagMaker()
            bagmaker.add_to_ignorelist(ignore.get_list())
            bagmaker.add_to_ignorelist(nltk.corpus.stopwords.words('english'))
            bagmaker.add_to_ignorelist(list(string.punctuation))

        Args:
            :param to_ignore: List of strings to ignore.
        """
        # wrap in list so can accept non-iterables
        to_ignore = [to_ignore] if isinstance(to_ignore, str) else to_ignore
        self._ignore = list(self._ignore)
        [self._ignore.append(i) for i in to_ignore]
        self._ignore = set(self._ignore)
        self._ignore = tuple(self._ignore)


class IgnoreDawgFilter(IFilter):
    """
        Detects whether the string is in the ignore dawg and returns
        a boolean so it can be removed.
        TODO: Make this better
        """
    __name__ = 'IgnoreDawgFilter'

    def __init__(self):
        super().__init__()
        self._ignore = ()

    def run(self, word, **kwargs):
        """Run the filter using a dawg instead of tuple"""
        if word in self._ignore_dawg:
            return False
        else:
            return True

    def add_to_ignorelist(self, to_ignore):
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
        # wrap in list so can accept non-iterables
        to_ignore = [to_ignore] if isinstance(to_ignore, str) else to_ignore
        self._ignore = list(self._ignore)
        [self._ignore.append(i) for i in to_ignore]
        self._ignore = set(self._ignore)
        self._ignore = tuple(self._ignore)
        self._ignore_dawg = dawg.DAWG(self._ignore)


class URLFilter(IFilter):
    """
    Detects whether the string is a url and returns
    a boolean so it can be removed.
    NB, This is tweet url specific
    TODO: Make this better
    """
    __name__ = 'URLFilter'

    patterns = ( '//t.co', 'http')

    def __init__(self):
        # covers https
        super().__init__()

    @classmethod
    def keep( cls, word ):
        for p in cls.patterns:
            if p in word:
                raise ExcludedString

        return True

    def run(self, word, **kwargs):
        return type(self).keep(word)
        # for p in type(self).patterns:
        #     if p in word:
        #         return False
        # return True


class UsernameFilter(IFilter):
    """
    Filters out twitter usernames (and empty strings)
    """
    __name__ = 'UsernameFilter'

    def __init__(self):
        super().__init__()

    def run(self, word, **kwargs):
        try:
            assert (type(word) is str)
            if word[0] == '@':
                raise ExcludedString
            if len(word) >= 2 and word[0:1] == '.@':
                raise ExcludedString
            return True
        except IndexError:
            raise ExcludedString
            # print('index error: %s' % word)

class NumeralFilter(IFilter):
    """
    Filters out all non-alphanumeric characters
    """
    __name__ = 'NumeralFilter'

    def __init__(self):
        super().__init__()

    def run(self, word, **kwargs):
        if isinstance(word, str):
            if word.isnumeric():
                raise ExcludedString
            # return word.isalpha( )
        else:
            raise ExcludedString

        return True



class PunctuationFilter(IFilter):
    """
    Filters out punctuation
    Given a text string, remove all non-alphanumeric characters
     Uses Unicode definition of alphanumeric
    """

    __name__ = 'PunctuationFilter'

    def __init__(self):
        super().__init__()

        # self.pattern = re.compile(r'\W+', re.UNICODE)
        self.to_avoid = tuple(string.punctuation)

    def run(self, word, **kwargs):
        """
        Checks whether word is in a list of punctuation.
        NB, it returns the inverse value because the processor
        removes things for which a filter returns false
        """
        word = str(word).strip()
        # return not self.pattern.match(word)
        if word in self.to_avoid:
            raise ExcludedString

        return True


class StopwordFilter(IFilter):
    """
    Filters out stopwords
    Given a text string, remove all non-alphanumeric characters
     Uses Unicode definition of alphanumeric
    """

    __name__ = 'StopwordFilter'

    def __init__(self):
        self.to_avoid = tuple(english_stops)

    def run(self, word, **kwargs):
        """
        Checks whether word is in a list of punctuation.
        NB, it returns the inverse value because the processor
        removes things for which a filter returns false
        """
        word = str(word).strip()
        if word in self.to_avoid:
            raise ExcludedString

        return True
