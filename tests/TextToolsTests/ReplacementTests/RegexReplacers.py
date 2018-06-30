import unittest

from TextProcessingTools.Replacement import RegexReplacers


class RegexReplacersText( unittest.TestCase ):
    def test_contractions( self ):
        test = [("Can't", 'cannot'), ("http", ''), ("https", '')]

        for target, expect in test:
            r = RegexReplacers.replace_contractions(target)
            self.assertEqual( expect, r )


if __name__ == '__main__':
    unittest.main()
