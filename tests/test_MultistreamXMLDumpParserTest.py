import threading
import unittest
import os

from compat import File, TreeSet

from parser import MultistreamXMLDumpParser, XMLDumpParser, MultistreamFilter


class MultistreamXMLDumpParserTest(unittest.TestCase):

    multistreamDump = None
    multistreamDumpIndex = 0
    pageCount = 0.  # atomic
    subject = None

    class MyXMLDumpParser(XMLDumpParser):

        def __init__(self, outer):
            self.outer = outer

        def onElementStart(self, name, handler):
            if "page" == name:
                with self.outer._lock:
                    self.outer.pageCount += 1  # atomic

        def onElementEnd(self, name, handler):
            pass

        def register(self, pageParser):
            pass

        def getPageParsers(self):
            return None

    def setUp(self):  # throws Exception
        super().setUp()

        self.pageCount = 0  # atomic
        self._lock = threading.Lock()

        self.multistreamDump = File(os.path.join(os.getcwd(), "resources"),
                                    "enwiktionary-20150224-pages-articles-multistream.xml.bz2")
        self.multistreamDumpIndex = File(os.path.join(os.getcwd(), "resources"),
                                         "enwiktionary-20150224-pages-articles-multistream-index.txt.bz2")
        self.subject = MultistreamXMLDumpParser(MultistreamXMLDumpParserTest.MyXMLDumpParser(self))

    def _testParseWithOffsets(self):  # throws Exception
        offsets = TreeSet()
        offsets.add(654)
        offsets.add(261373)
        self.subject.parseFile(self.multistreamDump, offsets)
        with self._lock:
            self.assertEqual(200, self.pageCount)

    def testCollectOffsets(self):  # throws Exception

        def accept(_, _pageId, pageTitle):
            return pageTitle == "nonsense" or pageTitle == "abattoir"

        filter_ = type("_MultistreamFilter", (MultistreamFilter,), {"accept": accept})

        offsets = self.subject.collectOffsets(self.multistreamDumpIndex, filter_())

        self.assertEqual(2, len(offsets.items()))
        self.assertTrue(654 in offsets)
        self.assertTrue(261373 in offsets)
