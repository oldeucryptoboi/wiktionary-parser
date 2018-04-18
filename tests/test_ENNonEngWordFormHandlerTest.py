import unittest

from api.util.GrammaticalGender import GrammaticalGender
from parser.en.components import ENNonEngWordFormHandler
from tests import *


class ENNonEngWordFormHandlerTest(unittest.TestCase, WordFormHandlerTest):

    def setUp(self):  # throws Exception
        super().setUp()
        self.handler = ENNonEngWordFormHandler()

    def testHandleDeNoun(self):
        self.assertGender(GrammaticalGender.NEUTER, "{{de-noun|n|Boots|gen2=Bootes|Boote|Bötchen}}")

    def testHandlePtNoun(self):
        self.assertGender(GrammaticalGender.MASCULINE, "{{pt-noun|m|s}}")

    def testHandlePtNounWithTwoGendersDashed(self):
        self.assertGender(GrammaticalGender.MASCULINE, "{{pt-noun|m-f|s}}")
        # TODO: need to change data model to reflect nouns having more than one gender

    def testHandlePtNounWithTwoGenders(self):
        self.assertGender(GrammaticalGender.MASCULINE, "{{pt-noun|mf|s}}")
        # TODO: need to change data model to reflect nouns having more than one gender

    def testHandleLaNounMasculine(self):
        self.assertGender(GrammaticalGender.MASCULINE, "{{la-noun|fīlius|filii|fīliī|m|second}}")

    def testHandleLaNounFeminine(self):
        self.assertGender(GrammaticalGender.FEMININE, "{{la-noun|casa|casae|casae|f|first}}")

    def testHandleLaNounNeutrum(self):
        self.assertGender(GrammaticalGender.NEUTER, "{{la-noun|vīnum|vini|vīnī|n|second}}")

    def testHandleHead(self):
        self.assertGender(GrammaticalGender.FEMININE, "{{head|fr|noun|g=f}}")

    def testHandleHeadWithSeparateGenderSpecifier(self):
        self.assertGender(GrammaticalGender.FEMININE, "{{head|pt|plural}} {{g|f}}")

    def testGetRawHeadwordLineHeadTemplate(self):  # throws Exception
        self.assertTrue(self.handler.parse("{{head|fr|foo}}"))
        self.assertEqual("{{head|fr|foo}}", self.handler.getRawHeadwordLine())

    def testGetRawHeadwordLineNounTemplate(self):  # throws Exception
        self.assertTrue(self.handler.parse("{{de-noun|foo}}"))
        self.assertEqual("{{de-noun|foo}}", self.handler.getRawHeadwordLine())

    def assertGender(self, expectedGender, line):
        self.assertTrue("could not parse " + line, self.handler.parse(line))
        self.assertEqual(expectedGender, self.handler.getGenders()[0])
