import string
import unittest

from TextProcessingTools.TextTools.Filtration import Filters
from TextProcessingTools.TextTools.Processors.Exceptions import ExcludedString

from nltk.corpus import stopwords
english_stops = set(stopwords.words('english'))

class InheritanceTest(unittest.TestCase):
    def test_expected_inheritance(self):
        obj = Filters.NumeralFilter()
        print(type(obj))
        # self.assertTrue(inspect.isclass(obj))
        # self.assertTrue(issubclass(obj, Filters.IFilter))
        self.assertTrue( isinstance( obj, Filters.IFilter ) )


class IgnoreListFilterTest(unittest.TestCase):
    def test_add_to_ignorelist_list(self):
        self.obj = Filters.IgnoreListFilter()
        test = ['taco', 'cat', 'fish']
        self.obj.add_to_ignorelist(test)
        self.assertIsInstance(self.obj._ignore, tuple)
        [self.assertIn(w, self.obj._ignore) for w in test]

    def test_add_to_ignorelist_string(self):
        self.obj = Filters.IgnoreListFilter()
        test = 'taco'
        self.obj.add_to_ignorelist(test)
        self.assertIsInstance(self.obj._ignore, tuple)
        self.assertEqual(self.obj._ignore, tuple([test]))


class NumeralFilterTest(unittest.TestCase):
    def test_happy_path_is_string(self):
        self.obj = Filters.NumeralFilter()
        test = 'taco'
        self.assertRaises()

        self.assertTrue(self.obj.run(test))

    def test_happy_path_not_string(self):
        self.obj = Filters.NumeralFilter()
        test = 5
        self.assertFalse(self.obj.run(test))

    def test_happy_path_num_string(self):
        self.obj = Filters.NumeralFilter()
        test = '5'
        self.assertFalse(self.obj.run(test))


class PunctuationFilterTest(unittest.TestCase):
    def test_happy_path_string(self):
        self.obj = Filters.PunctuationFilter()
        test = 'taco'
        self.assertTrue(self.obj.run(test))


    def test_happy_path_punctuation(self):
        self.obj = Filters.PunctuationFilter()
        for i in list(string.punctuation):
            with self.assertRaises(ExcludedString):
                self.obj.run(i)
            # self.assertFalse(self.obj.run(i))

    def test_happy_path_num_string(self):
        self.obj = Filters.PunctuationFilter()
        test = '5'
        self.assertTrue(self.obj.run(test))

    def test_happy_path_number(self):
        self.obj = Filters.PunctuationFilter()
        test = 5
        self.assertTrue(self.obj.run(test))


class URLFilterTest(unittest.TestCase):
    """
    Removes some urls
    """
    def setUp(self):
        self.object = Filters.URLFilter()

    def test_clean(self):
        test = [('taco', True), ('//t.co', False), ('cat', True),
                ('//t.co', False),
                ('http', False),
                ('https', False)
                ]
        for t in test:
            if t[1]:
                self.assertTrue(self.object.run(t[0]))
            else:
                with self.assertRaises(ExcludedString):
                    self.object.run( t[0 ] )


class UsernameFilterTest(unittest.TestCase):
    def setUp(self):
        self.object = Filters.UsernameFilter()

    def test_clean(self):
        test = [('taco', True), ('@taco', False), ('cat', True), ('@cat', False), ('', False)]
        for t in test:
            if t[1]:
                self.assertTrue(self.object.run(t[0]))
            else:
                with self.assertRaises(ExcludedString):
                    self.object.run( t[0 ] )


class NumeralFilterTest(unittest.TestCase):
    def setUp(self):
        self.object = Filters.NumeralFilter()

    def test_clean(self):
        test = [('taco', True), (1, False), ('cat', True), ('3', False), (['taco'], False)]

        for t in test:
            if t[1]:
                self.assertTrue(self.object.run(t[0]))
            else:
                with self.assertRaises(ExcludedString):
                    self.object.run( t[0 ] )


class StopwordFilterTest(unittest.TestCase):
    def setUp(self):
        self.object = Filters.StopwordFilter()
        self.stopwords = english_stops

    def test_clean(self):
        for t in self.stopwords:
            with self.assertRaises(ExcludedString):
                self.object.run( t )



if __name__ == '__main__':
    unittest.main()
