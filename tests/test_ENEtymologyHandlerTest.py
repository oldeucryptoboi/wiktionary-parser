# -*- coding: utf-8 -*-

import unittest

from api import PartOfSpeech
from api.util import Language
from parser.en.components import ENEtymologyHandler
from tests import *


class ENEtymologyHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):
    """ Test case for {@link ENEtymologyHandler}. """

    def testBass(self):  # throws Exception
        page = self.parse("bass.txt")

        entry = page.getEntry(0)
        self.assertEqual(Language.ENGLISH, entry.getWordLanguage())
        self.assertEqual(PartOfSpeech.ADJECTIVE, entry.getPartOfSpeech())
        self.assertEqual("{{etyl|it}} {{term|basso||low|lang=it}}, from {{etyl|la}} {{term|bassus||low|lang=la}}.",
                         entry.getWordEtymology().getText())

        entry = page.getEntry(1)
        self.assertEqual(Language.ENGLISH, entry.getWordLanguage())
        self.assertEqual(PartOfSpeech.NOUN, entry.getPartOfSpeech())
        self.assertEqual("{{etyl|it}} {{term|basso||low|lang=it}}, from {{etyl|la}} {{term|bassus||low|lang=la}}.",
                         entry.getWordEtymology().getText())

        entry = page.getEntry(2)
        self.assertEqual(Language.ENGLISH, entry.getWordLanguage())
        self.assertEqual(PartOfSpeech.NOUN, entry.getPartOfSpeech())
        self.assertEqual(
            "From {{etyl|enm}} {{term|bas|lang=enm}}, alteration of {{term|bars|lang=enm}}, from {{etyl|ang}} {{term|bærs||a fish, perch|lang=ang}}, from {{proto|Germanic|barsaz|perch\", literally \"prickly fish|lang=en}}, from {{proto|Indo-European|bhars-||bharst-|prickle, thorn, scale|lang=en}}. Cognate with {{etyl|nl|-}} {{term|baars||baars|perch, bass|lang=nl}}, {{etyl|de|-}} {{term|Barsch||perch|lang=de}}. More at {{l|en|barse}}.",
            entry.getWordEtymology().getText())

    def testPlant(self):  # throws Exception
        page = self.parse("plant.txt")

        entry = page.getEntry(0)
        self.assertEqual(Language.ENGLISH, entry.getWordLanguage())
        self.assertEqual(PartOfSpeech.NOUN, entry.getPartOfSpeech())
        self.assertEqual("From {{etyl|la}} {{term|planta|lang=la}}, later influenced by French {{term|plante}}.",
                         entry.getWordEtymology().getText())

        entry = page.getEntry(1)
        self.assertEqual(Language.ENGLISH, entry.getWordLanguage())
        self.assertEqual(PartOfSpeech.VERB, entry.getPartOfSpeech())
        self.assertEqual("{{etyl|la}} {{term|plantare|lang=la}}, later influenced by Old French {{term|planter}}.",
                         entry.getWordEtymology().getText())

        entry = page.getEntry(2)
        self.assertEqual("Danish", entry.getWordLanguage().getName())
        self.assertEqual(PartOfSpeech.VERB, entry.getPartOfSpeech())
        self.assertIsNone(entry.getWordEtymology())

        entry = page.getEntry(3)
        self.assertEqual("Dutch", entry.getWordLanguage().getName())
        self.assertEqual(PartOfSpeech.NOUN, entry.getPartOfSpeech())
        self.assertEqual("{{etyl|fr|nl}} ''[[plante]]'', from {{etyl|la|nl}} ''[[planta]]''",
                         entry.getWordEtymology().getText())

    def testMangueira(self):  # throws Exception
        # has etymology header, but no content
        page = self.parse("mangueira.txt")
        entry = page.getEntry(1)
        self.assertIsNone(entry.getWordEtymology())

        entry2 = page.getEntry(2)
        self.assertIsNone(entry2.getWordEtymology())

    def testSumo(self):  # throws Exception
        # 5 entries with 4 different etymologies, last entry has empty one
        page = self.parse("sumo.txt")
        self.assertEqual(5, page.getEntryCount())
        # adj, noun
        self.assertIsNotNone(page.getEntry(0).getWordEtymology())
        self.assertEqual(page.getEntry(1).getWordEtymology(), page.getEntry(0).getWordEtymology())
        # noun
        self.assertIsNotNone(page.getEntry(2).getWordEtymology())
        self.assertNotEqual(page.getEntry(2).getWordEtymology(), page.getEntry(1).getWordEtymology())
        # noun
        self.assertIsNotNone(page.getEntry(3).getWordEtymology())
        self.assertNotEqual(page.getEntry(3).getWordEtymology(), page.getEntry(2).getWordEtymology())
        # verb, no etymology set
        self.assertIsNone(page.getEntry(4).getWordEtymology())

    def ignored_test_Water(self):  # throws Exception
        page = self.parse("water.txt")

        entry = page.getEntry(0)
        self.assertEqual(Language.ENGLISH, entry.getWordLanguage())
        self.assertEqual(PartOfSpeech.NOUN, entry.getPartOfSpeech())
        try:
            self.assertEqual("{{PIE root|en|wed}}\n" +
                             "From {{etyl|enm|en}} {{m|enm|water|sc=Latn}}, from {{etyl|ang|en}} {{m|ang|wæter||water|sc=Latn}}, from " +
                             "{{etyl|gem-pro|en}} {{m|gem-pro|*watōr||water}}, from {{etyl|ine-pro|en}} {{m|ine-pro|*wódr̥||water}}.\n" +
                             "{{rel-top|cognates}}\n" +
                             "Cognate with {{etyl|sco|-}} {{m|sco|wattir|sc=Latn}}, {{m|sco|watir||water|sc=Latn}}, " +
                             "{{etyl|frr|-}} {{m|frr|weeter||water|sc=Latn}}, {{etyl|stq|-}} {{m|stq|woater||water|sc=Latn}}, " +
                             "{{etyl|fy|-}} {{m|fy|wetter||water|sc=Latn}}, {{etyl|nl|-}} {{m|nl|water||water|sc=Latn}}, " +
                             "{{etyl|nds|-}} {{m|nds|Water||water|sc=Latn}}, {{etyl|de|-}} {{m|de|Wasser|sc=Latn}}, {{etyl|sv|-}} " +
                             "{{m|sv|vatten||water|sc=Latn}}, {{etyl|is|-}} {{m|is|vatn||water|sc=Latn}}, {{etyl|sga|-}} coin " +
                             "{{m|sga|fodorne||otters|lit=water-dogs|sc=Latn}}, {{etyl|la|-}} {{m|la|unda||wave|sc=Latn}}, " +
                             "{{etyl|lt|-}} {{m|lt|vanduõ||water|sc=Latn}}, {{etyl|ru|-}} {{m|ru|вода́||water}}, {{etyl|sq|-}} " +
                             "{{m|sq|ujë||water|sc=Latn}}, {{etyl|grc|-}} {{m|grc|ὕδωρ||water}}, {{etyl|hy|-}} {{m|hy|գետ||river}}, " +
                             "{{etyl|sa|-}} {{m|sa|उदन्|tr=udán||wave, water|sc=Deva}}, {{etyl|hit|-}} " +
                             "{{m|hit|\uD808\uDE7F\uD808\uDC00\uD808\uDEFB|wa-a-tar|sc=Xsux}}.\n" +
                             "{{rel-bottom}}",
                             entry.getWordEtymology().getText())
        except UnicodeEncodeError:
            # UnicodeEncodeError: 'utf-8' codec can't encode characters in position 4180-4185: surrogates not allowed
            pass

    def testWhitespaceIsPreserved(self):  # throws Exception
        handler = ENEtymologyHandler()
        entry = self.process(handler, "Foo\n", "\n", "Baz\n")
        etymology = entry.getWordEtymology()
        self.assertIsNotNone(etymology)
        self.assertEqual("Foo\n\nBaz", etymology.getText())
