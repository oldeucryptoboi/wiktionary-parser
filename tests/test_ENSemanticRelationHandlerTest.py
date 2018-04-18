import unittest
from compat import List

from api import RelationType
from parser.en.components import ENSemanticRelationHandler
from tests import *


class ENSemanticRelationHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):

    def testSynonymsRainCatsAndDogs(self):  # throws Exception
        page = self.parse("rain_cats_and_dogs.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "bucket", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "bucket down", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "chuck it down", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "rain buckets", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "rain pitchforks", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "pelt", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "piss down", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "pour", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "stream", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "teem", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsDictionary(self):  # throws Exception
        page = self.parse("dictionary.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getUnassignedSense().getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "wordbook", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsGoitrogenic(self):  # throws Exception
        page = self.parse("goitrogenic.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "antithyroid", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsPound(self):  # throws Exception
        page = self.parse("pound.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(5).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "£", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "pound sterling", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "punt", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsCallously(self):  # throws Exception
        page = self.parse("callously.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "carelessly", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "hardheartedly", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "indifferently", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "unfeelingly", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsWallpaper(self):  # throws Exception
        page = self.parse("wallpaper.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(3).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "desktop image", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "desktop pattern", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsLung(self):  # throws Exception
        page = self.parse("lung.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "bellows", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "lights", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsDrink(self):  # throws Exception
        page = self.parse("drink.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(2).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "gulp", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "imbibe", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "quaff", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "sip", iter_.next())
        # TODO: Implement Wikisaurus.
        # self.assertRelation(RelationType.SYNONYM, "Wikisaurus:drink", iter_.next())
        # self.assertFalse(iter_.hasNext())

    def testSynonymsShutUp(self):  # throws Exception
        page = self.parse("shut_up.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(6).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "be quiet", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "be silent", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "fall silent", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "hush", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "quieten down", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "shush", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "be quiet!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "can it!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "hush!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "put a sock in it!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "quiet!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "sh!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "shush!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "shut it!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "shut your face!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "shaddap", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "silence!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "st!", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "STFU", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsXray(self):  # throws Exception
        page = self.parse("X-ray.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(2).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "Röntgen radiation", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "Rontgen radiation", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "Roentgen radiation", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "Röntgen rays", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "Rontgen rays", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "Roentgen rays", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "X-ray radiation", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsAbdominal(self):  # throws Exception
        page = self.parse("abdominal.txt")
        entry = page.getEntry(1)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "Cypriniformes", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsAbreast(self):  # throws Exception
        page = self.parse("abreast.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "apprised", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "up to date/up-to-date", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsHead(self):  # throws Exception
        page = self.parse("head.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(13).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "headmaster", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "headmistress", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "principal", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsTermination(self):  # throws Exception
        page = self.parse("termination.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "concluding", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "ending", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "finishing", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "stoping", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "terminating", iter_.next())
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getSense(2).getRelations(RelationType.SYNONYM)).iterator()
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getSense(3).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "close", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "conclusion", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "end", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "finale", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "finish", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "stop", iter_.next())
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getSense(4).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "border", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "edge", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "end", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "limit", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "lip", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "rim", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "tip", iter_.next())
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getSense(5).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "consequence", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "outcome", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "result", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "upshot", iter_.next())
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getSense(6).getRelations(RelationType.SYNONYM)).iterator()
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getSense(7).getRelations(RelationType.SYNONYM)).iterator()
        self.assertRelation(RelationType.SYNONYM, "abortion", iter_.next())
        self.assertRelation(RelationType.SYNONYM, "induced abortion", iter_.next())
        self.assertFalse(iter_.hasNext())
        iter_ = List(entry.getUnassignedSense().getRelations(RelationType.SYNONYM)).iterator()
        self.assertFalse(iter_.hasNext())

    def testAntonymsKiefer(self):  # throws Exception
        page = self.parse("cow.txt")
        entry = page.getEntry(0)
        iter_ = List(entry.getSense(1).getRelations(RelationType.ANTONYM)).iterator()
        self.assertRelation(RelationType.ANTONYM, "bull", iter_.next())
        self.assertRelation(RelationType.ANTONYM, "ox", iter_.next())
        self.assertRelation(RelationType.ANTONYM, "steer", iter_.next())
        self.assertRelation(RelationType.ANTONYM, "heifer", iter_.next())
        self.assertFalse(iter_.hasNext())

    def testSynonymsCasa(self):  # throws Exception
        page = self.parse("casa.txt")
        entry = page.getEntry(0)
        synonyms = entry.getRelations(RelationType.SYNONYM)
        self.assertEqual(2, len(synonyms))

    def testSynonymsGranada(self):  # throws Exception
        page = self.parse("granada.txt")
        entry = page.getEntry(0)
        synonyms = entry.getRelations(RelationType.SYNONYM)
        self.assertEqual(3, len(synonyms))

        relations = entry.getSense(1).getRelations(RelationType.SYNONYM)  # pomegranate
        self.assertEqual(1, len(relations))
        self.assertEqual("romã", relations[0].getTarget())

        relations = entry.getSense(2).getRelations(RelationType.SYNONYM)  # hand grenade
        self.assertEqual(1, len(relations))
        self.assertEqual("granada de mão", relations[0].getTarget())

        relations = entry.getSense(3).getRelations(RelationType.SYNONYM)  # shell
        self.assertEqual(0, len(relations))

        relations = entry.getSense(4).getRelations(RelationType.SYNONYM)  # garnet
        self.assertEqual(1, len(relations))
        self.assertEqual("granate", relations[0].getTarget())

    def assertRelation(self, relationType, expected, actual):
        self.assertEqual(relationType, actual.getRelationType())
        self.assertEqual(expected, actual.getTarget())

    def testFindMatchingSenseWithMatch(self):  # throws Exception
        page = self.parse("casa.txt")
        entry = page.getEntry(0)
        sense = ENSemanticRelationHandler.findMatchingSense(entry, "home")
        self.assertIsNotNone(sense)
        self.assertEqual("{{l/en|home}} {{gloss|one’s own dwelling place}}", sense.getGloss().getText())

    def testFindMatchingSenseReturnsNullWithoutMatch(self):  # throws Exception
        page = self.parse("casa.txt")
        entry = page.getEntry(0)
        self.assertIsNone(ENSemanticRelationHandler.findMatchingSense(entry, "froobaz"))

    def testFindMatchingSenseWithoutMatchButMonosemousEntryReturnsEntry(self):  # throws Exception
        page = self.parse("goitrogenic.txt")
        entry = page.getEntry(0)
        self.assertIsNotNone(ENSemanticRelationHandler.findMatchingSense(entry, "froobaz"))

    def testFindMatchingSenseWithNullButMonosemousEntryReturnsEntry(self):  # throws Exception
        page = self.parse("goitrogenic.txt")
        entry = page.getEntry(0)
        self.assertIsNotNone(ENSemanticRelationHandler.findMatchingSense(entry, None))
