"""
Created by adam on 5/20/18
"""
from TextProcessingTools.TextProcessors import Tokenizers
from TextProcessingTools.TextTools.Processors.Parents import IProcessor

__author__ = 'adam'

if __name__ == '__main__':
    pass


class ParagraphProcessor( IProcessor ):
    """Operates on multiple sentence size pieces of text"""

    def set_initial_transforms(self, listOfModifiers, **kwargs):
        pass

    def __init__(self):
        super().__init__()
        self.tokenizer = Tokenizers.SentenceTokenizer()

    def process(self, to_process, **kwargs):
        """
        Split the tweet into sentences.
        By default returns a list
        if return_indexed is True, will return a list of tuples
        with the format ( ordinal position, string )
        :type to_process: object
         """
        self._process_kwargs(kwargs)

        sentences = self.tokenizer.process(to_process)

        if self.return_indexed:
            return [(idx, txt) for idx, txt in enumerate(sentences)]

        return sentences