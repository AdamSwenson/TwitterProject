"""
Created by adam on 11/23/16
"""
__author__ = 'adam'


from nltk.tokenize import word_tokenize, sent_tokenize


class ITokenizer:
    def process( self, item ): return NotImplementedError


class SentenceTokenizer( ITokenizer ):
    """Handles tokenization of sentences. Just a wrapper around nltk tokenizer"""
    def __init__( self ):
        super( ).__init__( )

    def process( self, item ):
        """Run the nltk sentence tokenizer on the item"""
        assert(isinstance(item, str))

        return sent_tokenize( item )


class WordTokenizer(ITokenizer):
    """Handles tokenization of words. Just a wrapper around nltk tokenizer"""
    def __init__( self ):
        super( ).__init__( )

    def process( self, item ):
        """Run the nltk word tokenizer on the item"""
        assert(isinstance(item, str))

        return word_tokenize( item )

