import unittest
import nltk

from TextTools.TextTools.Replacement import Modifiers as M


class CaseConverterTest( unittest.TestCase ):
    def test_happy_lower( self ):
        obj = M.CaseConverter()
        self.assertEqual( 'taco', obj.run( ' TACO' ) )

    def test_happy_upper( self ):
        obj = M.CaseConverter(False)
        self.assertEqual( 'TACO', obj.run( 'Taco ' ) )


class LemmatizerTest(unittest.TestCase):
    """
    Wrapper on nltk.stem.WordNetLemmatizer for lemmatizing words
    """
    def setUp(self):
        self.object = M.Lemmatizer()

    def test_process(self):
        self.assertIsInstance(self.object.lemmatizer, nltk.stem.WordNetLemmatizer)

    def test_process_excepts_if_not_string(self):
        self.assertRaises( AssertionError, self.object.run( 4 ) )


class PorterStemmerTest(unittest.TestCase):
    def setUp(self):
        self.object = M.PorterStemmer()

    def test_process(self):
        self.assertIsInstance(self.object.stemmer, nltk.stem.PorterStemmer)

    def test_process_excepts_if_not_string(self):
        self.assertRaises( AssertionError, self.object.run( 4 ) )



if __name__ == '__main__':
    unittest.main( )
