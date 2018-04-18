import unittest

from compat import List
from tests import *


class ENReferenceHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):
    """ Test case for {@link ENReferenceHandler}. """

    def testAbalone(self):  # throws Exception
        page = self.parse("abalone.txt")
        entry = page.getEntry(0)
        actualIter = List(entry.getReferences()).iterator()
        self.assertEqual("{{wikisource1911Enc|Abalone}}", actualIter.next().getText())
        self.assertEqual("{{pedialite|Abalone}}", actualIter.next().getText())
        self.assertEqual("{{R:American Heritage 2000|abalone}}", actualIter.next().getText())
        self.assertEqual("{{R:Dictionary.com|abalone}}", actualIter.next().getText())
        self.assertEqual("{{R:WordNet 2003|abalone}}", actualIter.next().getText())
        self.assertFalse(actualIter.hasNext())

    def testAbate(self):  # throws Exception
        page = self.parse("abate.txt")
        entry = page.getEntry(0)
        actualIter = List(entry.getReferences()).iterator()
        self.assertEqual("{{R:OneLook}}", actualIter.next().getText())
        self.assertEqual("{{R:Webster 1913}}", actualIter.next().getText())
        self.assertFalse(actualIter.hasNext())

        entry = page.getEntry(1)
        actualIter = List(entry.getReferences()).iterator()
        self.assertEqual("{{R:OneLook}}", actualIter.next().getText())
        self.assertEqual("{{R:Webster 1913}}", actualIter.next().getText())
        self.assertFalse(actualIter.hasNext())

        entry = page.getEntry(2)
        actualIter = List(entry.getReferences()).iterator()
        self.assertFalse(actualIter.hasNext())

    def testBoat(self):  # throws Exception
        page = self.parse("boat.txt")
        entry = page.getEntry(0)
        actualIter = List(entry.getReferences()).iterator()
        self.assertEqual(
            "Weisenberg, Michael (2000) ''[http://www.poker1.com/mcu/pokerdictionary/mculib_dictionary_info.asp The Official Dictionary of Poker].''  MGI/Mike Caro University.  ISBN 978-1880069523",
            actualIter.next().getText())
        self.assertFalse(actualIter.hasNext())

        entry = page.getEntry(1)
        actualIter = List(entry.getReferences()).iterator()
        self.assertFalse(actualIter.hasNext())
