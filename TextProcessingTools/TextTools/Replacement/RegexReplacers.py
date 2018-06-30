"""
Created by adam on 5/20/18
"""
__author__ = 'adam'

import re

contraction_patterns = [
    (r'//t.co', ''),
    (r'https|http', ''),
    (r'won\'t', 'will not'),
    (r'Won\'t', 'will not'),
    (r'can\'t', 'cannot'),
    (r'Can\'t', 'cannot'),
    (r'i\'m', 'i am'),
    (r'I\'m', 'i am'),
    (r'ain\'t', 'is not'),
    (r'Ain\'t', 'is not'),
    (r'(\w+)\'ll', '\g<1> will'),
    (r'(\w+)n\'t', '\g<1> not'),
    (r'(\w+)\'ve', '\g<1> have'),
    (r'(\w+t)\'s', '\g<1> is'),
    (r'(\w+)\'re', '\g<1> are'),
    (r'(\w+)\'d', '\g<1> would'),
]


#
# contraction_patterns = tuple([(re.compile(a), b) for a, b in contraction_patterns])


def replace_contractions( text ):
    """
  Executes regex replacement on text input based on stored
  regex patterns.
  By default will replace contractions
  Properties:
      _patterns: Tuple of compiled regex replacement patterns to apply
  Replaces regular expression in a text.
  >>> replace_contractions("can't is a contraction")
  'cannot is a contraction'
  """
    for (pattern, repl) in contraction_patterns:
        text = re.sub( pattern, repl, text )
    return text


class Rep( object ):
    patterns = [ ]
    contraction_patterns = [
        # (r'^b$', ''),
        (r'//t.co', ''),
        (r'https|http', ''),
        (r'won\'t', 'will not'),
        (r'Won\'t', 'will not'),
        (r'can\'t', 'cannot'),
        (r'Can\'t', 'cannot'),
        (r'i\'m', 'i am'),
        (r'I\'m', 'i am'),
        (r'ain\'t', 'is not'),
        (r'Ain\'t', 'is not'),
        (r'(\w+)\'ll', '\g<1> will'),
        (r'(\w+)n\'t', '\g<1> not'),
        (r'(\w+)\'ve', '\g<1> have'),
        (r'(\w+t)\'s', '\g<1> is'),
        (r'(\w+)\'re', '\g<1> are'),
        (r'(\w+)\'d', '\g<1> would'),
    ]

    @classmethod
    def _initialize_regex( cls ):
        if len( cls.patterns ) == 0:
            cls.patterns = tuple( [ (re.compile( a ), b) for a, b in contraction_patterns ] )

    @classmethod
    def replace( cls, text ):
        """
      Executes regex replacement on text input based on stored
      regex patterns.
      By default will replace contractions
      Properties:
          _patterns: Tuple of compiled regex replacement patterns to apply
      Replaces regular expression in a text.
      >>> replace_contractions("can't is a contraction")
      'cannot is a contraction'
      """
        cls._initialize_regex()
        for (pattern, repl) in cls.patterns:
            text = re.sub( pattern, repl, text )
        return text

#
# if __name__ == '__main__':
#     import doctest
#     doctest.testmod()
