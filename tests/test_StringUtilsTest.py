import unittest
from parser.util import StringUtils


class TestStringUtils(unittest.TestCase):

    def testStrip(self):
        self.assertEqual("", StringUtils.strip("", " :"))
        self.assertEqual("white space", StringUtils.strip(" white space  ", " "))
        self.assertEqual(" Section ", StringUtils.strip("=== Section ===", "{}=:"))
        self.assertEqual("Section", StringUtils.strip("=== Section ===", "{}=: "))
        self.assertEqual("Section", StringUtils.strip("{{Section}}", "{}=:"))

    def testCompileIndexSet(self):
        indexSet = StringUtils.compileIndexSet("")
        self.assertTrue(indexSet.remove(-1))
        self.assertTrue(indexSet.isEmpty())
        indexSet = StringUtils.compileIndexSet("[]")
        self.assertTrue(indexSet.remove(-1))
        self.assertTrue(indexSet.isEmpty())
        indexSet = StringUtils.compileIndexSet("?")
        self.assertTrue(indexSet.remove(-1))
        self.assertTrue(indexSet.isEmpty())

        indexSet = StringUtils.compileIndexSet("[1]")
        self.assertTrue(indexSet.remove(1))
        self.assertTrue(indexSet.isEmpty())
        indexSet = StringUtils.compileIndexSet("[20]")
        self.assertTrue(indexSet.remove(20))
        self.assertTrue(indexSet.isEmpty())
        indexSet = StringUtils.compileIndexSet(" [ 2 ] ")
        self.assertTrue(indexSet.remove(2))
        self.assertTrue(indexSet.isEmpty())

        indexSet = StringUtils.compileIndexSet("[1,3, 4,15 , 10,17]")
        self.assertTrue(indexSet.remove(1))
        self.assertTrue(indexSet.remove(3))
        self.assertTrue(indexSet.remove(4))
        self.assertTrue(indexSet.remove(15))
        self.assertTrue(indexSet.remove(10))
        self.assertTrue(indexSet.remove(17))
        self.assertTrue(indexSet.isEmpty())

        indexSet = StringUtils.compileIndexSet("[3-5]")
        self.assertTrue(indexSet.remove(3))
        self.assertTrue(indexSet.remove(4))
        self.assertTrue(indexSet.remove(5))
        self.assertTrue(indexSet.isEmpty())

        indexSet = StringUtils.compileIndexSet("[ 2,3-5, 4 a ,10-11,4 ,5@]")
        self.assertTrue(indexSet.remove(2))
        self.assertTrue(indexSet.remove(3))
        self.assertTrue(indexSet.remove(4))
        self.assertTrue(indexSet.remove(5))
        self.assertTrue(indexSet.remove(10))
        self.assertTrue(indexSet.remove(11))
        self.assertTrue(indexSet.isEmpty())

    def testCleanText(self):
        self.assertEqual("foo", StringUtils.cleanText("[[foo]] "))

    def testStripMarkup(self):
        self.assertEqual("foo", StringUtils.stripMarkup("[[foo]]"))


if __name__ == '__main__':
    unittest.main()
