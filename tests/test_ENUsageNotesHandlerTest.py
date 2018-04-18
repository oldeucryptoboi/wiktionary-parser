import unittest

from tests import *


class ENUsageNotesHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):

    def testParseBatsman(self):  # throws Exception
        page = self.parse("batsman.txt")
        entry = page.getEntries()[1]
        self.assertEqual("The term batsman is applied to both male and female cricketers; [[batswoman]] is much rarer.",
                         entry.getUsageNotes().getText())

    def testParsePound(self):  # throws Exception
        page = self.parse("pound.txt")
        entry = page.getEntries()[0]
        self.assertEqual(
            "* Internationally, the \"pound\" has most commonly referred to the UK pound. The other currencies were usually distinguished in some way, e.g., the \"Irish pound\" or the \"punt\".\n" +
            "* In the vicinity of each other country calling its currency the pound among English speakers the local currency would be the \"pound\", with all others distinguished, e.g., the \"British pound\".",
            entry.getUsageNotes().getText())

        self.assertEqual("Manx English uses this word uncountably.",
                         page.getEntries()[1].getUsageNotes().getPlainText())
        self.assertIsNone(page.getEntries()[2].getUsageNotes())
        self.assertIsNone(page.getEntries()[3].getUsageNotes())

    def testDreier(self):  # throws Exception
        page = self.parse("dreier.txt")
        entry = page.getEntries()[0]
        self.assertEqual(
            "Only in adjectival use and only when no article or pronoun is preceding. More at {{term|drei|lang=de}}.",
            entry.getUsageNotes().getText())
        self.assertIsNone(page.getEntries()[1].getUsageNotes())
