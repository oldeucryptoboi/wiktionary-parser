import unittest
import collections

from api.entry import WiktionaryPage
from parser.components import CategoryHandler
from parser.util import ParsingContext
from errors import IllegalStateException


class TestCategoryHandler(unittest.TestCase):

    CATEGORY_FOO = "[[Category:Foo]]"
    CATEGORY_BAR = "[[Category:Bar]]"
    CATEGORY_COLON_FOO = "[[:Category:Foo]]"
    # https://www.mediawiki.org/wiki/Help:Categories#Sort_key
    CATEGORY_FOO_SORT_KEY = "[[Category:Foo|sort]]"

    categoryHandler = None

    def setUp(self):  # throws Exception
        self.categoryHandler = CategoryHandler("Category")

    def testCanHandleNoMatch(self):  # throws Exception
        self.assertFalse(self.categoryHandler.canHandle("XXX"))

    def testCanHandleMatchSingleLine(self):  # throws Exception
        self.assertTrue(self.categoryHandler.canHandle(self.CATEGORY_FOO))

    def testCanHandleMatchTrailingWhitespace(self):  # throws Exception
        self.assertTrue(self.categoryHandler.canHandle(self.CATEGORY_FOO+"    "))

    def testCanHandleMatchLeadingWhitespace(self):  # throws Exception
        self.assertTrue(self.categoryHandler.canHandle("   "+self.CATEGORY_FOO))

    def testCanHandleMatchEmptyString(self):  # throws Exception
        self.assertFalse(self.categoryHandler.canHandle(""))

    def testCanHandleMatchNull(self):  # throws Exception
        self.assertFalse(self.categoryHandler.canHandle(None))

    def testNoMatchThrowsIllegalStateException(self):  # throws Exception
        self.assertRaises(IllegalStateException, self.parseCategories, "XXX")

    def testEmptyStringThrowsIllegalStateException(self):  # throws Exception
        self.assertRaises(IllegalStateException, self.parseCategories, "")

    def testNoneThrowsIllegalStateException(self):  # throws Exception
        self.assertRaises(IllegalStateException, self.parseCategories, *[None])

    def testSingleCategory(self):  # throws Exception
        self.assertEqual(["Foo"], self.parseCategories(self.CATEGORY_FOO))

    def testSingleCategoryColon(self):  # throws Exception
        self.assertEqual(["Foo"], self.parseCategories(self.CATEGORY_COLON_FOO))

    def testSingleCategorySortKey(self):  # throws Exception
        self.assertEqual(["Foo"], self.parseCategories(self.CATEGORY_FOO_SORT_KEY))

    def testSingleCategoryLeadingWhitespace(self):  # throws Exception
        self.assertEqual(["Foo"], self.parseCategories("      "+self.CATEGORY_FOO))

    def testSingleCategoryTrailingWhitespace(self):  # throws Exception
        self.assertEqual(["Foo"], self.parseCategories(self.CATEGORY_FOO+"        "))

    def testMultipleCategories(self):  # throws Exception
        self.assertEqual(collections.Counter(["Bar", "Foo"]),
                         collections.Counter(self.parseCategories(self.CATEGORY_FOO, self.CATEGORY_BAR)))

    def testMultipleDuplicatedCategories(self):  # throws Exception
        self.assertEqual(["Foo"], self.parseCategories(self.CATEGORY_FOO, self.CATEGORY_FOO))

    def testMultipleCategoriesSingleLine(self):  # throws Exception
        self.assertEqual(collections.Counter(["Bar", "Foo"]),
                         collections.Counter(self.parseCategories(self.CATEGORY_FOO + " " + self.CATEGORY_BAR)))
        self.assertEqual(collections.Counter(["Bar", "Foo"]),
                         collections.Counter(self.parseCategories("  "+self.CATEGORY_FOO + "    " + self.CATEGORY_BAR+" ")))

    def parseCategories(self, *input_):
        page = WiktionaryPage()
        context = ParsingContext(page)
        for s in input_:
            self.categoryHandler.processHead(s, context)
        self.categoryHandler.fillContent(context)
        categories = page.getCategories()
        sorted(categories)
        return categories


if __name__ == '__main__':
    unittest.main()
