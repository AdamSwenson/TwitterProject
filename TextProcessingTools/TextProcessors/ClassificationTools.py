# Used for WordFilters

from TextProcessingTools.TextTools.Replacement.Modifiers import *


class PartOfSpeechClassification(object):
    """
    Tools for classifying part of speech
    """

    @classmethod
    def get_pos_tags(cls, word_list):
        """
        Tags each word with its part of speech
        Args:
            word_list: Word bag (list of strings)
        Returns:
            Returns a list of tuples with the format (word, pos) where pos is the wordnet pos tag
        """
        return [(word, cls._convert_treebank_tag_to_wordnet_pos(tag)) for word, tag in nltk.pos_tag(word_list)]

    @classmethod
    def _convert_treebank_tag_to_wordnet_pos(cls, tag):
        """
        The nltk.pos_tag() is trained on the treebank corpus. So it returns
        a different representation of the part of speech than the wordnet
        lemmatizer is expecting. This handles the conversion.

        Args:
            tag: String penn_treebank tag

        Returns:
            Wordnet part of speech tag or None
        """

        def is_noun(tag):
            return tag in ['NN', 'NNS', 'NNP', 'NNPS']

        def is_verb(tag):
            return tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']

        def is_adverb(tag):
            return tag in ['RB', 'RBR', 'RBS']

        def is_adjective(tag):
            return tag in ['JJ', 'JJR', 'JJS']

        if is_adjective(tag):
            return wn.ADJ
        elif is_noun(tag):
            return wn.NOUN
        elif is_adverb(tag):
            return wn.ADV
        elif is_verb(tag):
            return wn.VERB
        return None


if __name__ == '__main__':
    pass
