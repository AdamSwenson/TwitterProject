import unittest

from TextTools.Filtration import Filters
from TextTools.Replacement import Modifiers
from StatisticalTools import Counters as C

filters = [
    Filters.UsernameFilter(),
    Filters.PunctuationFilter(),
    Filters.URLFilter(),
    Filters.NumeralFilter()
]

modifiers = [
    Modifiers.WierdBPrefixConverter(),
    Modifiers.CaseConverter()
]


class SelectedCounterTests(unittest.TestCase):
    def setUp(self):
        self.obj = C.SelectedWordCounter()
        self.obj.add_filters(filters)
        self.obj.add_modifiers(modifiers)

    def test_process_count(self):
        test = "My cat eats food of cat"
        self.obj.set_words_to_count(['my', 'cat', 'eats'])
        expected = {'my': 1, 'cat': 2, 'eats': 1}
        self.obj.process(test)

        # check
        for k in expected.keys():
            self.assertEqual(self.obj.counts[k], expected[k])


class WordCounterTests(unittest.TestCase):
    def setUp(self):
        self.obj = C.WordCounter()
        self.obj.add_filters(filters)
        self.obj.add_modifiers(modifiers)

    def test_process_count(self):
        test = "My cat eats food of cat"
        expected = {'my': 1, 'cat': 2, 'eats': 1, 'food': 1, 'of': 1}
        self.obj.process(test)

        # check
        for k in expected.keys():
            self.assertEqual(self.obj.counts[k], expected[k])

    def test_process_output(self):
        test = "My cat eats food of cat"
        # prep
        expected_output = [k.lower() for k in test.split(' ')]
        expected_output.sort()

        # call
        output = self.obj.process(test)

        # check
        output.sort()
        self.assertListEqual(output, expected_output)

    def test_process_map(self):
        # prep
        testId = 43
        test = "My cat eats food of cat"
        # setup the test data
        expected = {'my': 1, 'cat': 2, 'eats': 1, 'food': 1, 'of': 1}
        for k in expected.keys():
            # a list with only the test id
            expected[k.lower()] = [testId]
        # account for the second 'cat'
        expected['cat'].append(testId)

        # call
        self.obj.process(test, testId)

        # check
        for k in expected.keys():
            self.assertEqual(self.obj.map[k], expected[k])


if __name__ == '__main__':
    unittest.main()
