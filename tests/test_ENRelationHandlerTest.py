import unittest

from api import RelationType
from parser.en.components import ENRelationHandler
from tests import *
from compat import List


class ENRelationHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):
    """ Test case for {@link ENRelationHandler}. """

    def testParseRelation(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        relation = self.processFirst(handler, "* {{l|en|target}}")
        self.assertEqual(RelationType.DERIVED_TERM, relation.getRelationType())
        self.assertEqual("target", relation.getTarget())
        self.assertIsNone(relation.getLinkType())

    def testParseRelationNoWhitespace(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        self.assertEqual("target", self.processFirst(handler, "*{{l|en|target}}").getTarget())
        self.assertEqual("target", self.processFirst(handler, "*[[target]]").getTarget())

    def testParseRelationExtraWhitespace(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        self.assertEqual("target", self.processFirst(handler, "*   {{l|en|target}}").getTarget())
        self.assertEqual("target", self.processFirst(handler, "*  [[target]]").getTarget())

    def testParseRelationLinkedWithTemplate(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        self.assertEqual("target", self.processFirst(handler, "* {{l|en|target}}").getTarget())

    def testParseRelationLinkedWithSquareBrackets(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        self.assertEqual("target", self.processFirst(handler, "* [[target]]").getTarget())

    def testParseRelationList(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        relations = self.process(handler,
                                 "* {{l|en|target1}}",
                                 "* [[target2]]",
                                 ).getRelations()
        self.assertEqual(2, len(relations))
        self.assertEqual("target1", relations[0].getTarget())
        self.assertEqual("target2", relations[1].getTarget())

    def testParseRelationListWithTemplateHeaderAndFooter(self):  # throws Exception
        handler = ENRelationHandler(RelationType.DERIVED_TERM, "Derived terms")
        relations = self.process(handler,
                                 "{{rel-top3|Terms derived from ''foo''}}",
                                 "* {{l|en|target1}}",
                                 "* [[target2]]",
                                 "{{rel-mid3}}",
                                 "* [[target3]]",
                                 "* [[target4]]",
                                 "{{rel-bottom}}",
                                 ).getRelations()
        self.assertEqual(4, len(relations))

    def testDerivedTermsMonday(self):  # throws Exception
        page = self.parse("Monday.txt")
        entry = page.getEntry(0)
        relations = entry.getRelations(RelationType.DERIVED_TERM)
        self.assertEqual(46, len(relations))
        self.assertEqual("Ash Monday", relations[0].getTarget())
        self.assertEqual("Whitsun Monday", relations[-1].getTarget())

    def testDerivedTermsCasa(self):  # throws Exception
        page = self.parse("casa.txt")
        entry = page.getEntry(0)
        derived = entry.getUnassignedSense().getRelations(RelationType.DERIVED_TERM)
        self.assertEqual(33, len(derived))
        # make sure we don't have derived terms assigned to a sense
        for sense in entry.getSenses():
            self.assertEqual(0, len(sense.getRelations(RelationType.DERIVED_TERM)))

    def testRelationsDescendantsDid(self):  # throws Exception
        page = self.parse("did.txt")
        entry = page.getEntry(2)
        iter_ = List(entry.getUnassignedSense().getRelations(RelationType.DESCENDANT)).iterator()
        self.assertTrue(iter_.hasNext())
        self.assertRelation(RelationType.DESCENDANT, "Welsh: dydd", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testRelationsDescendantVaranda(self):  # throws Exception
        page = self.parse("varanda.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getUnassignedSense().getRelations(RelationType.DESCENDANT)).iterator()
        self.assertRelation(RelationType.DESCENDANT, "Hindi: बरामदा", iter_.next())
        self.assertRelation(RelationType.DESCENDANT, "Hindi: बरण्डा", iter_.next())
        self.assertRelation(RelationType.DESCENDANT, "English: veranda", iter_.next())
        self.assertRelation(RelationType.DESCENDANT, "English: verandah", iter_.next())
        self.assertRelation(RelationType.DESCENDANT, "French: véranda", iter_.next())
        self.assertFalse(iter_.hasNext())

    def assertRelation(self, relationType, expected, actual):
        self.assertEqual(relationType, actual.getRelationType())
        self.assertEqual(expected, actual.getTarget())

    def processFirst(self, handler, *body):
        relations = self.process(handler, *body).getRelations()
        self.assertFalse(not relations)
        return relations[0]


if __name__ == '__main__':
    unittest.main()
