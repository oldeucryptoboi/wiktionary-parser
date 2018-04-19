import time
import unittest

from api.util import Language
from compat import *
from errors import *

from parser import IWiktionaryEntryParser, WiktionaryDumpParser, WritableDBWiktionaryEdition, WiktionaryArticleParser

from tests import *


class WiktionaryArticleParserTest(unittest.TestCase, WiktionaryTestCase):

    # noinspection PyMissingConstructor
    class _WiktionaryDumpParser(WiktionaryDumpParser, IWiktionaryEntryParser):

        def __init__(self):  # throws WiktionaryException
            super().__init__()
            self.pages = dict()
            self.register(WiktionaryArticleParser(None, self))

        def getPages(self):
            return self.pages

        def parse(self, page, text):  # throws WiktionaryException
            self.pages[page] = text

    def setUp(self):  # throws Exception
        super().setUp()
        self.testDump = File(self.RESOURCE_PATH, "WiktionaryDumpParserTest.xml")

    def testParsedInformation(self):
        parser = self._WiktionaryDumpParser()
        parser.parseFile(self.testDump)
        dumpInfo = parser.getDumpInfo()
        self.assertEqual(2, dumpInfo.getProcessedPages())
        self.assertEqual(2, len(parser.getPages()))

        pageIter = List(parser.getPages().keys()).iterator()
        page = pageIter.next()
        self.assertEqual("Page 1", page.getTitle())
        self.assertEqual(9, page.getId())
        self.assertEqual(10763, page.getRevision())
        self.assertEqual("2004-09-17T08:23:57Z", self.format8601(page.getTimestamp()))
        self.assertEqual("TJ", page.getAuthor())
        self.assertEqual("Text 1", parser.getPages().get(page))

        page = pageIter.next()
        self.assertEqual("Page 2", page.getTitle())
        self.assertEqual(10, page.getId())
        self.assertEqual(10764, page.getRevision())
        self.assertEqual("2004-09-17T08:34:29Z", self.format8601(page.getTimestamp()))
        self.assertEqual("TJ", page.getAuthor())
        self.assertEqual("Text 2\n\n      Test Test", parser.getPages().get(page))

        self.assertFalse(pageIter.hasNext())

    def ignored_test_DatabaseCreation(self):  # throws InterruptedException

        # Parse to empty directory.
        emptyDir = File(self.workDir, "empty/")
        emptyDir.mkdir()
        db = WritableDBWiktionaryEdition(emptyDir, False)
        WiktionaryDumpParser(WiktionaryArticleParser(db)).parseFile(self.testDump)
        self.assertParsedData(emptyDir)

        # Parse to non-existing directory.
        newDir = File(self.workDir, "new/")
        db = WritableDBWiktionaryEdition(newDir, False)
        WiktionaryDumpParser(WiktionaryArticleParser(db)).parseFile(self.testDump)
        self.assertParsedData(newDir)

        # Parse to existing, non-empty directory; allow overwrite.
        overwriteDir = File(self.workDir, "overwrite/")
        db = WritableDBWiktionaryEdition(overwriteDir, True)
        WiktionaryDumpParser(WiktionaryArticleParser(db)).parseFile(self.testDump)
        version = File(overwriteDir, "wiktionary.properties").lastModified()
        self.assertParsedData(overwriteDir)
        time.sleep(1000)  # necessary to compare timestamps!
        db = WritableDBWiktionaryEdition(overwriteDir, True)
        WiktionaryDumpParser(WiktionaryArticleParser(db)).parseFile(self.testDump)
        self.assertParsedData(overwriteDir)
        newVersion = File(overwriteDir, "wiktionary.properties").lastModified()
        self.assertTrue(version < newVersion)

        # Parse to existing, non-empty directory; permit overwrite.

        version = newVersion
        try:
            db = WritableDBWiktionaryEdition(overwriteDir, False)
            WiktionaryDumpParser(WiktionaryArticleParser(db)).parseFile(self.testDump)
            self.fail("WiktionaryException expected")
        except WiktionaryException:
            pass

        self.assertParsedData(overwriteDir)
        newVersion = File(overwriteDir, "wiktionary.properties").lastModified()
        self.assertTrue(version == newVersion)

        # Parsing more than once with the same parser is (currently) not allowed.
        multipleDir = File(self.workDir, "multiple/")
        db = WritableDBWiktionaryEdition(multipleDir, True)
        parser = WiktionaryDumpParser(WiktionaryArticleParser(db))
        parser.parseFile(self.testDump)
        self.assertParsedData(multipleDir)
        try:
            parser.parseFile(self.testDump)
            self.fail("IllegalStateException expected")
        except IllegalStateException:
            pass

        self.assertParsedData(multipleDir)

        # Parse to erroneous path.
        try:
            db = WritableDBWiktionaryEdition(File("/../:", ""), True)
            WiktionaryDumpParser(WiktionaryArticleParser(db)).parseFile(self.testDump)
            self.fail("WiktionaryException expected")
        except WiktionaryException:
            pass

    def test_LargeDump(self):
        parser = self._WiktionaryDumpParser()
        parser.parseFile(File(self.RESOURCE_PATH, "WiktionaryDumpParserLargeFileTest.xml"))
        self.assertEqual(30000, len(parser.getPages()))

    def testResolveLanguage(self):
        self.assertEqual(Language.ENGLISH, WiktionaryDumpParser().resolveLanguage(
            baseURL="http://en.wiktionary.org/wiki/Wiktionary:Main_Page"))
        # self.assertEqual(Language.GERMAN, WiktionaryDumpParser().resolveLanguage(
        #     baseURL="http://de.wiktionary.org/wiki/Wiktionary:Hauptseite"))
        # self.assertEqual(Language.RUSSIAN, WiktionaryDumpParser().resolveLanguage(
        #     baseURL="http://ru.wiktionary.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"))
        self.assertIsNone(WiktionaryDumpParser().resolveLanguage(
            baseURL="foobar"))

    def assertParsedData(self, parsedData):
        # self.assertTrue(File(parsedData, "00000000.jdb").exists())
        # self.assertTrue(File(parsedData, "je.lck").exists())
        # self.assertTrue(File(parsedData, "je.info.0").exists())
        self.assertTrue(File(parsedData, "wiktionary.properties").exists())

    @classmethod
    def format8601(cls, date):
        return date
