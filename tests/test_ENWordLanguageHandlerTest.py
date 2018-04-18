import unittest
from compat import *

from api import PartOfSpeech
from api.util import Language
from tests import *


class ENWordLanguageHandlerTest(unittest.TestCase, ENWiktionaryEntryParserTest):

    def testAbele(self):  # throws Exception
        page = self.parse("abele.txt")
        entryIter = List(page.getEntries()).iterator()
        self.assertEntry(Language.ENGLISH, PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.findByName("Novial"), PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertFalse(entryIter.hasNext())

    def testBass(self):  # throws Exception
        page = self.parse("bass.txt")
        entryIter = List(page.getEntries()).iterator()
        self.assertEntry(Language.ENGLISH, PartOfSpeech.ADJECTIVE, 1, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.NOUN, 5, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.findByName("Romansch"), PartOfSpeech.ADJECTIVE, 1, entryIter.next())
        self.assertFalse(entryIter.hasNext())

    def testDid(self):  # throws Exception
        page = self.parse("did.txt")
        entryIter = List(page.getEntries()).iterator()
        self.assertEntry(Language.findByName("Translingual"), PartOfSpeech.NUMBER, 1, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.VERB, 1, entryIter.next())
        self.assertEntry(Language.findByName("Old Welsh"), PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertFalse(entryIter.hasNext())

    def testIt_s(self):  # throws Exception
        page = self.parse("it_s.txt")
        entryIter = List(page.getEntries()).iterator()
        self.assertEntry(Language.ENGLISH, PartOfSpeech.CONTRACTION, 2, entryIter.next())
        self.assertFalse(entryIter.hasNext())

    def testMay(self):  # throws Exception
        page = self.parse("may.txt")
        entryIter = List(page.getEntries()).iterator()
        self.assertEntry(Language.ENGLISH, PartOfSpeech.VERB, 4, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.VERB, 1, entryIter.next())
        self.assertEntry(Language.findByName("Crimean Tatar"), PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.findByName("Kurdish"), PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.findByName("Mapudungun"), PartOfSpeech.ADVERB, 1, entryIter.next())
        self.assertEntry(Language.findByName("Tagalog"), PartOfSpeech.VERB, 1, entryIter.next())
        self.assertEntry(Language.findByName("Tatar"), PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertFalse(entryIter.hasNext())

    def testPortmanteau(self):  # throws Exception
        page = self.parse("portmanteau.txt")
        entryIter = List(page.getEntries()).iterator()
        self.assertEntry(Language.ENGLISH, PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.NOUN, 1, entryIter.next())
        self.assertEntry(Language.ENGLISH, PartOfSpeech.ADJECTIVE, 1, entryIter.next())
        self.assertFalse(entryIter.hasNext())

    def assertEntry(self, language, partOfSpeech, senseCount, entry):
        self.assertEqual(language, entry.getWordLanguage())
        self.assertEqual(partOfSpeech, entry.getPartOfSpeech())
        self.assertEqual(senseCount, entry.getSenseCount())
