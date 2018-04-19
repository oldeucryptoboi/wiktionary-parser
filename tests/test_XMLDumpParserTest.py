import os
import unittest
import xml

from parser import XMLDumpParser
from errors import WiktionaryException, IOException
from compat import File


class XMLDumpParserTest(unittest.TestCase):
    """ Test case for {@link XMLDumpParser}. """

    def setUp(self):  # throws Exception {
        super().setUp()

        self.parser = type("_XMLDumpParser", (XMLDumpParser,), {
            "onElementStart": (lambda self, name, handler: None),
            "onElementEnd": (lambda self, name, handler: None),
            "register": (lambda self, pageParser: None),
            "getPageParsers": (lambda self: None)})()

    class _XMLDumpParser(XMLDumpParser):
        def __init__(self, outer, expectedValues):
            self.outer = outer
            self.expectedValues = expectedValues

        def register(self, pageParser):
            pass

        def getPageParsers(self):
            return None

        def onParserStart(self):
            super().onParserStart()
            self.outer.assertEqual(self.expectedValues.pop(0), "onParserStart")

        def onElementStart(self, name, handler):
            self.outer.assertEqual(self.expectedValues.pop(0), "onElementStart: " + name)

        def onElementEnd(self, name, handler):
            self.outer.assertEqual(self.expectedValues.pop(0), "onElementEnd: " + name)

        def onParserEnd(self):
            self.outer.assertEqual(self.expectedValues.pop(0), "onParserEnd")
            self.outer.assertTrue(not self.expectedValues)
            super().onParserEnd()

    def testParsedInformation(self):
        """<dump_parser_test>
          <header>
            <param name="param1" value="value1" />
            <param name="param1" value="value2" />
          </header>
          <element id="1">
            Some text content
          </element>
          <element id="2">
            Some text content
          </element>
        </dump_parser_test>*"""

        expectedValues = list()
        expectedValues.append("onParserStart")
        expectedValues.append("onElementStart: dump_parser_test")
        expectedValues.append("onElementStart: header")
        expectedValues.append("onElementStart: param")
        expectedValues.append("onElementEnd: param")
        expectedValues.append("onElementStart: param")
        expectedValues.append("onElementEnd: param")
        expectedValues.append("onElementEnd: header")
        expectedValues.append("onElementStart: element")
        expectedValues.append("onElementEnd: element")
        expectedValues.append("onElementStart: element")
        expectedValues.append("onElementEnd: element")
        expectedValues.append("onElementEnd: dump_parser_test")
        expectedValues.append("onParserEnd")

        self.parser = XMLDumpParserTest._XMLDumpParser(self, expectedValues)
        self.parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "XMLDumpParserTest.xml"))
        self.assertTrue(not expectedValues)

    def testBzip2Stream(self):
        expectedValues = list()
        expectedValues.append("onParserStart")
        expectedValues.append("onElementStart: dump_parser_test")
        expectedValues.append("onElementStart: header")
        expectedValues.append("onElementStart: param")
        expectedValues.append("onElementEnd: param")
        expectedValues.append("onElementStart: param")
        expectedValues.append("onElementEnd: param")
        expectedValues.append("onElementEnd: header")
        expectedValues.append("onElementStart: element")
        expectedValues.append("onElementEnd: element")
        expectedValues.append("onElementStart: element")
        expectedValues.append("onElementEnd: element")
        expectedValues.append("onElementEnd: dump_parser_test")
        expectedValues.append("onParserEnd")

        self.parser = XMLDumpParserTest._XMLDumpParser(self, expectedValues)
        self.parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "XMLDumpParserTest.xml.bz2"))
        self.assertTrue(not expectedValues)

    def testErrors(self):

        # Missing file.
        try:
            self.parser.parseFile(File("", "missing_dump$@%.xml"))
            self.fail("WiktionaryException/IOException expected")
        except (IOException, WiktionaryException) as e:
            self.assertTrue(isinstance(e, IOException) or isinstance(e, WiktionaryException))

        # Invalid XML.
        try:
            self.parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "XMLDumpParserErrorXMLTest.xml"))
            self.fail("WiktionaryException/SAXException expected")
        except xml.sax.SAXException as e:
            self.assertTrue(isinstance(e, xml.sax.SAXParseException))

        # Empty Bzip2 file.
        try:
            self.parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "XMLDumpParserErrorEmptyTest.xml.bz2"))
            self.fail("WiktionaryException/IOException expected")
        except xml.sax.SAXException as e:
            self.assertTrue(isinstance(e, xml.sax.SAXParseException))

        # Erroneous Bzip2 header.
        try:
            self.parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "XMLDumpParserErrorHeaderTest.xml.bz2"))
            self.fail("WiktionaryException/IOException expected")
        except xml.sax.SAXException as e:
            self.assertTrue(isinstance(e, xml.sax.SAXParseException))

    def testParseMultistreamWithNormalParser(self):  # throws Exception
        self.parser.parseFile(File(os.path.join(os.getcwd(), "resources"), "enwiktionary-20150224-pages-articles-multistream.xml.bz2"))

