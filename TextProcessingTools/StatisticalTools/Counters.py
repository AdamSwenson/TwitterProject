"""
Created by adam on 3/9/18
"""
import TextProcessingTools.TextTools.Processors.SingleWordProcessors

__author__ = 'adam'

import pickle

import TextProcessingTools.TextTools.Processors as Processors
import TextProcessingTools.TextProcessors.Tokenizers as Tokenizers


class ICounter(object):

    def __init__(self):
        self.map = {}
        self.counts = {}

    def add_filters(self, filters):
        """
        Adds list of filters to the processor module.
        NB, we let the processor module worry about type checks
        """
        [self.word_processor.add_filters(f) for f in filters]

    def add_modifiers(self, modifiers):
        """
        Adds list of modifiers to the processor module.
        NB, we let the processor module worry about type checks
        """
        for m in modifiers:
            self.word_processor.add_modifiers(m)

    @property
    def initializedKeys(self):
        lst = list(self.counts.keys()) + list(self.map.keys())
        return set(lst)

    def _update(self, word, identifier=None):
        """increment the count and add to the mapping, if applicable"""
        self.counts[word] += 1
        if identifier is not None:
            self.map[word].append(identifier)

    def process(self, text_to_process, identifier=None):
        raise NotImplementedError

    def save_map_to_file(self, filePath):
        pickle.dump(self.map, filePath)
        print("Pickled map to %s" % filePath)


class WordCounter(ICounter):
    """This class handles simple frequency calculations of a bunch of text """

    def __init__(self):
        super().__init__()
        self.wordTokenizer = Tokenizers.WordTokenizer()
        self.word_processor = TextProcessingTools.TextTools.Processors.SingleWordProcessors.SingleWordProcessor()

    def process(self, text_to_process, identifier=None):
        """Tokenizes, filters, modifies, and counts the input text"""
        words = self.wordTokenizer.process(text_to_process)
        return [self._count(w, identifier) for w in words]

    def _count(self, word, identifier=None):
        """Processes a result of word tokenization and updates the count appropriately"""
        # run filters on the string
        word = self.word_processor.process(word)
        if word is not None:
            if word not in self.initializedKeys:
                # create an empty list in map and
                # count entry set to 0
                self._create(word, identifier)
            # update the store
            self._update(word, identifier)
            return word

    def _create(self, word, identifier=None):
        # create a new entry
        self.counts[word] = 0
        # add to the map
        self.map[word] = []


class SelectedWordCounter(ICounter):
    """This class handles simple frequency calculations of a bunch of text """

    def __init__(self):
        super().__init__()
        self.wordTokenizer = Tokenizers.WordTokenizer()
        self.word_processor = TextProcessingTools.TextTools.Processors.SingleWordProcessors.SingleWordProcessor()

    def set_words_to_count(self, list_of_words_to_count):
        for word in list_of_words_to_count:
            self.map[word] = []
            self.counts[word] = 0

    def process(self, text_to_process, identifier=None):
        """Tokenizes, filters, modifies, and counts the input text"""
        words = self.wordTokenizer.process(text_to_process)
        return [self._count(w, identifier) for w in words]

    def _count(self, word, identifier=None):
        """Processes a result of word tokenization and updates the count appropriately"""
        # run filters on the string
        word = self.word_processor.process(word)
        if word is not None:
            if word in self.initializedKeys:
                # update the store. otherwise ignore
                self._update(word, identifier)
            return word


if __name__ == '__main__':
    pass
