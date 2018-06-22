import unittest

from faker import Faker

import TextTools.ReplacementInterfaces
from TextTools.Filtration import Filters
from TextTools.Replacement import Modifiers
import TextTools.Processors.ParagraphProcessors
import TextTools.Processors.SingleWordProcessors

fake = Faker()


class SingleWordProcessorTests(unittest.TestCase):
    def setUp(self):
        self.obj = TextTools.Processors.SingleWordProcessors.SingleWordProcessor()
        self.faker = Faker()

    def test_happy_process(self):
        self.obj._modifiers = [ Modifiers.CaseConverter(), Modifiers.RegexpReplacer() ]
        self.obj._filters = [ Filters.NumeralFilter(), Filters.PunctuationFilter() ]

        # should make lowercase and replace contraction
        self.assertEqual('taco', self.obj.process('Taco'))
        self.assertEqual("will not", self.obj.process("WON'T"))
        self.assertEqual(None, self.obj.process(43))
        self.assertEqual(None, self.obj.process('.'))

        # patterns which had problems in testing of program
        self.assertEqual(None, self.obj.process('..'))

    def test_happy_run_modifiers(self):
        modifiers = [ Modifiers.CaseConverter(), Modifiers.RegexpReplacer() ]
        [ self.assertTrue( isinstance( m, TextTools.ReplacementInterfaces.IModifier ) ) for m in modifiers ]
        self.obj._modifiers = modifiers

        self.assertTrue(len(self.obj._modifiers) is len(modifiers))

        # should make lowercase and replaces contraction
        self.assertEqual("will not", self.obj.process("WON'T"))

    def test_happy_run_filters(self):
        test = self.faker.word()
        nf = Filters.NumeralFilter()
        print(type(nf))
        self.assertTrue( isinstance( nf, Filters.IFilter ) )
        self.obj.add_filters(nf)
        self.obj.add_filters( Filters.PunctuationFilter() )

        self.assertTrue(len(self.obj._filters) is 2)

        self.assertEqual(True, self.obj._run_filters(test))
        self.assertEqual(False, self.obj._run_filters('5'))
        self.assertEqual(False, self.obj._run_filters('.'))

    def test_process_none_loaded(self):
        test = self.faker.word()
        result = self.obj.process(test)
        self.assertEqual(test, result)

    def test_run_modifiers_no_modifiers(self):
        test = self.faker.word()
        result = self.obj._run_modifiers(test)
        self.assertEqual(test, result)

    def test_run_filters_no_filters(self):
        test = self.faker.word()
        result = self.obj._run_filters(test)
        self.assertEqual(True, result)


class ParagraphProcesorTests(unittest.TestCase):
    def setUp(self):
        self.object = TextTools.Processors.ParagraphProcessors.ParagraphProcessor()

    def test_process_default(self):
        test = fake.text()
        # call
        result = self.object.process(test)

        # check
        self.assertIsInstance(result, list, "Returns list")
        self.assertTrue(len(result) > 0)

    def test_process_return_indexed(self):
        test = fake.text()

        # call
        result = self.object.process(test, return_indexed=True)
        print(result)

        # check
        self.assertIsInstance(result, list, "Returns list")
        self.assertTrue(len(result) > 0)
        for i in range(0, len(result)):
            self.assertIsInstance(result[i], tuple, "List contains tuples")
            self.assertEqual(i, result[i][0], "First member of returned tuple is index")


if __name__ == '__main__':
    unittest.main()
