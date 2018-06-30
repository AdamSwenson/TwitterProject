"""
Created by adam on 5/20/18
"""
import re

from TextProcessingTools.TextTools.Processors.Parents import IProcessor
from TextProcessingTools.TextTools.Replacement import RegexReplacers
from TextProcessingTools.TextTools.Processors import Exceptions

__author__ = 'adam'

if __name__ == '__main__':
    pass


class SingleWordProcessor( IProcessor ):
    """
    Runs filtration and transformation operations on one
    string at a time returning either the modified string
    or None
    """

    # pattern = re.compile(r'\W+', re.UNICODE)

    def set_initial_transforms(self, listOfModifiers, **kwargs):
        pass

    def __init__(self):
        super().__init__()

    def check_excluded( self, text ):
        exclude = ('b', "''", "'s")

        if len(text) == 0:
            raise Exceptions.ExcludedString
        if text in exclude:
            raise Exceptions.ExcludedString


    def process(self, to_process, **kwargs):
        """
        Processes one word at a time by first running all modifiers
        in stack and then running all filters in stack

        Args:
            to_process: Single word to process
        """
        try:
            if not isinstance(to_process, str): raise ValueError('Non-string')

            text = self._run_modifiers(to_process)

            # will raise an exception if the text is to be filtered
            self._run_filters(text)

            self.check_excluded(text)

            return text

        except Exceptions.ExcludedString:
            # The string has been filtered out
            return None

        except ValueError:
            print('non-string passed in')
            return None

    # def process(self, to_process, **kwargs):
    #     """
    #     Processes one word at a time by first running all modifiers
    #     in stack and then running all filters in stack
    #
    #     Args:
    #         to_process: Single word to process
    #     """
    #     try:
    #         if not isinstance(to_process, str): raise ValueError('Non-string')
    #
    #         text = to_process.strip().lower()
    #
    #         text = RegexReplacers.Rep.replace(text)
    #
    #         if len(text) == 0:
    #             return None
    #
    #         # pattern = re.compile(r'\W+', re.UNICODE)
    #
    #         if re.search(r'\W+', text):
    #             return None
    #
    #         # Run filters and return tokens which aren't screened out
    #         if self._run_filters(text) is True:
    #             # print( 'filter complete: %s' % to_process )
    #             return text
    #         else:
    #             # Return none if the token was filtered out
    #             return None
    #     except ValueError:
    #         print('non-string passed in')
    #         return None

    def _run_modifiers(self, text):
        if len(self._modifiers) > 0:
            for modifier in self._modifiers:
                text = modifier.run(text)
                # print( text )
        return text

    def _run_filters(self, word):
        """Runs all filters on the word. If none of them
        return False, then returns true
        """
        if len(self._filters) > 0:
            for f in self._filters:
                f.run(word)
                # print( 'running filter \n filtername: %s \n word: %s' % (f.__name__, word) )
                # if f.run(word) is False:
                    # print( 'filter %s failed: %s' % (f.__name__, word) )
                    # return False
        return True
