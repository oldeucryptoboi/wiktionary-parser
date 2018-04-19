import os
import unittest
import datetime

from api.util import Language
from compat import File
from errors import IllegalStateException

from parser import *
from parser.util import IDumpInfo


class WiktionaryDumpParserTest(unittest.TestCase):
    """ Test case for {@link WiktionaryDumpParser}."""

    class MyWiktionaryDumpParser(WiktionaryDumpParser):

        def __init__(self, outer, expectedValues):
            super().__init__()
            self.outer = outer
            self.expectedValues = expectedValues

        def setBaseURL(self, baseURL):
            self.outer.assertEqual(self.expectedValues.pop(0), "setBaseURL: " + baseURL)

        def addNamespace(self, namespace):
            self.outer.assertEqual(self.expectedValues.pop(0), "addNamespace: " + namespace)

        def onPageStart(self):
            self.outer.assertEqual(self.expectedValues.pop(0), "onPageStart")

        def onPageEnd(self):
            self.outer.assertEqual(self.expectedValues.pop(0), "onPageEnd")

        def setPageId(self, pageId):
            self.outer.assertEqual(self.expectedValues.pop(0), "setPageId: " + str(pageId))

        def setTitle(self, title):
            self.outer.assertEqual(self.expectedValues.pop(0), "setTitle: " + title)

        def setAuthor(self, author):
            self.outer.assertEqual(self.expectedValues.pop(0), "setAuthor: " + author)

        def setRevision(self, revisionId):
            self.outer.assertEqual(self.expectedValues.pop(0), "setRevision: " + str(revisionId))

        def setTimestamp(self, timestamp):
            try:
                datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
            except ValueError:
                timestamp = ""

            self.outer.assertEqual(self.expectedValues.pop(0), "setTimestamp: " + ("null" if not timestamp else str(timestamp)))

        def setText(self, text):
            self.outer.assertEqual(self.expectedValues.pop(0), "setText: " + text)

    def testParsedInformation(self):
        expectedValues = list()

        expectedValues.append("setBaseURL: http://de.wiktionary.org/wiki/Wiktionary:Hauptseite")
        expectedValues.append("addNamespace: Diskussion")
        expectedValues.append("onPageStart")
        expectedValues.append("setTitle: Page 1")
        expectedValues.append("setPageId: 9")
        expectedValues.append("setRevision: 10763")
        expectedValues.append("setTimestamp: 2004-09-17T08:23:57Z")
        expectedValues.append("setAuthor: TJ")
        expectedValues.append("setText: Text 1")
        expectedValues.append("onPageEnd")
        expectedValues.append("onPageStart")
        expectedValues.append("setTitle: Page 2")
        expectedValues.append("setPageId: 10")
        expectedValues.append("setRevision: 10764")
        expectedValues.append("setTimestamp: 2004-09-17T08:34:29Z")
        expectedValues.append("setAuthor: TJ")
        expectedValues.append("setText: Text 2\n\n      Test Test")
        expectedValues.append("onPageEnd")

        parser = WiktionaryDumpParserTest.MyWiktionaryDumpParser(self, expectedValues)
        parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "WiktionaryDumpParserTest.xml"))
        self.assertTrue(not expectedValues)

    def testParseEmptyFields(self):
        expectedValues = list()
        expectedValues.append("onPageStart")
        expectedValues.append("setTitle: ")
        expectedValues.append("setPageId: 0")
        expectedValues.append("setRevision: 0")
        expectedValues.append("setTimestamp: null")
        expectedValues.append("setText: ")
        expectedValues.append("onPageEnd")
        expectedValues.append("onPageStart")
        expectedValues.append("setTimestamp: null")
        expectedValues.append("onPageEnd")

        parser = WiktionaryDumpParserTest.MyWiktionaryDumpParser(self, expectedValues)
        parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "WiktionaryDumpParserNullTest.xml"))

    def testParseTimestamp(self):  # throws Exception
        expected = "1956-03-17T21:30:15Z"
        parser = WiktionaryDumpParserTest.MyWiktionaryDumpParser(self, None)
        self.assertEqual(expected, parser.parseTimestamp("1956-03-17T21:30:15Z"))
        pass

    class EmptyParser(IWiktionaryPageParser):
        def onParserStart(self, dumpInfo):
            pass

        def onSiteInfoComplete(self, dumpInfo):
            pass

        def onParserEnd(self, dumpInfo):
            pass

        def onClose(self, dumpInfo):
            pass

        def onPageStart(self):
            pass

        def onPageEnd(self):
            pass

        def setAuthor(self, author):
            pass

        def setRevision(self, revisionId):
            pass

        def setTimestamp(self, timestamp):
            pass

        def setPageId(self, pageId):
            pass

        def setTitle(self, title, namespace):
            pass

        def setText(self, text):
            pass

    def _testParseMultistream(self):  # throws Exception

        pageIds = list()
        siteInfo = [IDumpInfo]

        def onSiteInfoComplete(self, dumpInfo):
            if siteInfo[0] is None:
                siteInfo[0] = dumpInfo
            else:
                raise IllegalStateException("received onSiteInfoComplete more than once")

        def setPageId(self, pageId):
            pageIds.append(pageId)

        parser = type("_EmptyParser", (WiktionaryDumpParser, WiktionaryDumpParserTest.EmptyParser), {
            "onSiteInfoComplete": onSiteInfoComplete,
            "setPageId": setPageId})()

        multistreamDump = File(os.path.join(os.getcwd(), "resources"), "enwiktionary-20150224-pages-articles-multistream.xml.bz2")
        multistreamDumpIndex = File(os.path.join(os.getcwd(), "resources"), "enwiktionary-20150224-pages-articles-multistream-index.txt.bz2")

        parser.parseMultistream(
            multistreamDump,
            multistreamDumpIndex,
            MultistreamFilter.IncludingNames("aardvark"))

        self.assertIsNotNone("did not parse siteInfo", siteInfo[0])
        self.assertEqual(Language.ENGLISH, siteInfo[0].getDumpLanguage())

        self.assertEqual(100, len(pageIds))
        first = pageIds[0]
        last = pageIds[-1]
        self.assertEqual(177, first)
        self.assertEqual(306, last)
