import unittest
import collections

from parser.en.components import WordList
from errors import NullPointerException


class WordListTest(unittest.TestCase):

    def testParseEmptyLine(self):  # throws Exception
        parsed = WordList.parse("")
        self.assertEqual(0, len(parsed))

    def testParseNoneLine(self):  # throws Exception
        self.assertRaises(NullPointerException, WordList.parse, None)

    def testWordListImplementsIterable(self):
        list_ = WordList(None, ["1", "2"])
        iter_ = list_.iterator()
        self.assertTrue(iter_.hasNext())
        self.assertEqual("1", iter_.next())
        self.assertTrue(iter_.hasNext())
        self.assertEqual("2", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testParseLineWithOneWord(self):  # throws Exception
        parsed = WordList.parse("foo")
        self.assertEqual(["foo"], parsed.words)

    def testParseCommaSeparatedLine(self):  # throws Exception
        parsed = WordList.parse("foo, baz, fruz")
        self.assertEqual(3, len(parsed))
        self.assertEqual(collections.Counter(["foo", "baz", "fruz"]), collections.Counter(parsed.words))

    def testParseLineWithCorrectlyFormattedComment(self):  # throws Exception
        parsed = WordList.parse("(''sense one''): foo, baz, fruz")
        self.assertEqual(3, len(parsed))
        self.assertEqual(collections.Counter(["foo", "baz", "fruz"]), collections.Counter(parsed.words))
        self.assertEqual("sense one", parsed.comment)

    def testParseLineWithMalformedComment(self):  # throws Exception
        parsed = WordList.parse("(sense one) foo, baz, fruz")
        self.assertEqual(3, len(parsed))
        self.assertEqual(collections.Counter(["foo", "baz", "fruz"]), collections.Counter(parsed.words))
        self.assertEqual("sense one", parsed.comment)

    def testParseLineWithCommentFormattedAsTemplate(self):
        parsed = WordList.parse("{{sense|one|two}} [[foo]]")
        self.assertEqual("one|two", parsed.comment)
        self.assertEqual(["foo"], parsed.words)

    def testOnlyExtractLinkedComponentsOneItem(self):
        parsed = WordList.parse(" {{l/pt|casa}}")
        self.assertEqual(["casa"], parsed.words)

    def testOnlyExtractLinkedComponentsOneItemWithoutInitialWhitespace(self):
        parsed = WordList.parse("{{l/pt|casa}}")
        self.assertEqual(["casa"], parsed.words)

    def testOnlyExtractLinkedComponentsTwoItems(self):
        parsed = WordList.parse(" {{l/pt|casa}}, [[casa de banho]]")
        self.assertEqual(collections.Counter(["casa", "casa de banho"]), collections.Counter(parsed.words))

    def ignore_test_OnlyExtractLinkedComponents(self):
        # TODO: currently gets parsed incorrectly
        parsed = WordList.parse(" {{l/pt|casa roubada, trancas à porta}} — Robbed house, locked doors.")
        self.assertEqual(1, len(parsed))
        self.assertEqual(collections.Counter(["casa roubada, trancas à porta"]), collections.Counter(parsed.words))


if __name__ == '__main__':
    unittest.main()
