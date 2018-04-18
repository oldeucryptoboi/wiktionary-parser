import unittest
from parser.util import WordListProcessor


class TestWordListProcessor(unittest.TestCase):
    processor = None

    def setUp(self):  # throws Exception
        super().setUp()
        self.processor = WordListProcessor()

    def testSplitWordListWithNull(self):  # throws Exception
        words = self.processor.splitWordList(None)
        self.assertEqual(len(words), 0)

    def testSplitWordListWithNoItem(self):  # throws Exception
        words = self.processor.splitWordList("")
        self.assertEqual(len(words), 0)

    def testSplitWordListWithOneSimpleTemplateItem(self):  # throws Exception
        words = self.processor.splitWordList("{{l|fr|foo}}")
        self.assertEqual(len(words), 1)
        self.assertEqual(words[0], "foo")

    def testSplitWordListWithTwoSimpleTemplateItems(self):  # throws Exception
        words = self.processor.splitWordList("{{l|fr|foo}}, {{l|uk|bar}}")
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0], "foo")
        self.assertEqual(words[1], "bar")

    def testSplitWordListWithTwoSimpleTemplateItemsSlashedLinkTemplate(self):  # throws Exception
        words = self.processor.splitWordList("{{l/fr|foo}}, {{l/uk|bar}}")
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0], "foo")
        self.assertEqual(words[1], "bar")

    def testSplitWordListWithTwoComplexTemplateItems(self):  # throws Exception
        words = self.processor.splitWordList("{{l|hi|बरामदा|tr=barāmdā|sc=Deva}}, {{l|hi|बरण्डा|tr=baraṇḍā|sc=Deva}}")
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0], "बरामदा")
        self.assertEqual(words[1], "बरण्डा")


if __name__ == '__main__':
    unittest.main()
