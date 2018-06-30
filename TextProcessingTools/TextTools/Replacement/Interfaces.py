"""
Created by adam on 5/20/18
"""
__author__ = 'adam'


class IModifierList(object):
    """
    Interface for classes which act on a list of strings by modifying
    the input strings and returning a list of modified strings.
    Used for tasks like lemmatizing etc
    """

    def __init__(self):
        pass

    def run(self, wordbag, **kwargs):
        """
        Processes list of strings
        :param wordbag: List of strings to run
        :param kwargs:
        :return: List of strings, modified
        """
        raise NotImplementedError


class IModifier(object):
    """
    Interface for classes which modify the input string and return the
    modified string.
    Used for tasks like stemming lemmatizing etc
    """

    def __init__(self):
        pass

    def run(self, text, **kwargs):
        raise NotImplementedError

    def _check_is_single_word(self, text):
        """
        Some implmentations of IModifier allow for sentences. Others
        want just one word at a time. This is called by the latter
        and checks to make sure that it has the correct input
        :param text: String to screen for multiple words
        """
        assert (type(text) is str)
        assert (text.count(" ") is 0)


if __name__ == '__main__':
    pass

