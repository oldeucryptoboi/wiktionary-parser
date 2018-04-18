from xml.sax import handler

from parser import *

from compat import *
from errors import *


class XMLDumpParser(IWiktionaryDumpParser):
    """ Implementation of :@link IWiktionaryDumpParser for processing XML files
        downloaded from http://download.wikimedia.org/backup-index.html. There
        can be different specializations of this class that focus on a certain
        aspect of the dump, e.g., parsing the full text on the article pages and
        create an object structure from them, processing some aspects of
        the user pages, filtering the article pages, etc. The base class should
        be somewhat generic. """

    logger = Logger.getLogger("XMLDumpParser")

    class DefaultHandler(handler.ContentHandler, handler.ErrorHandler, handler.DTDHandler, handler.EntityResolver):

        def resolveEntity(self, publicId, systemId):  # throws IOException, SAXException
            return None

        def notationDecl(self, name, publicId, systemId):  # throws SAXException
            pass

        def unparsedEntityDecl(self, name, publicId, systemId, notationName):  # throws SAXException
            pass

        def setDocumentLocator(self, locator):  # throws SAXException
            pass

        def startDocument(self):  # throws SAXException
            pass

        def endDocument(self):  # throws SAXException
            pass

        def startPrefixMapping(self, prefix, uri):  # throws SAXException
            pass

        def endPrefixMapping(self, prefix):  # throws SAXException
            pass

        def startElement(self, name, attrs):  # throws SAXException
            pass

        def endElement(self, name):  # throws SAXException
            pass

        def characters(self, content):  # throws SAXException
            pass

        def ignorableWhitespace(self, whitespace):  # throws SAXException
            pass

        def processingInstruction(self, target, data):  # throws SAXException
            pass

        def skippedEntity(self, name):  # throws SAXException
            pass

        def warning(self, e):  # throws SAXException
            pass

        def error(self, e):  # throws SAXException
            pass

        def fatalError(self, e):  # throws SAXException
            pass

    def __init__(self):
        pass

    class XMLDumpHandler(DefaultHandler):

        def __init__(self, outer):
            self.outer = outer
            self.contentBuffer = ""
            self.tags = None

        def startDocument(self):  # throws SAXException :
            self.tags = Stack()
            self.contentBuffer = ""
            self.outer.onParserStart()
        
        def characters(self, content):  # throws SAXException
            self.contentBuffer += content
        
        def startElement(self, name, attrs):  # throws SAXException
            self.tags.append(name)
            self.contentBuffer = ""

            self.outer.onElementStart(name, self)

        def endElement(self, name):  # throws SAXException
            self.tags.pop()
            
            self.outer.onElementEnd(name, self)
        
        def endDocument(self):  # throws SAXException
            self.outer.onParserEnd()
        
        def getContents(self):
            """ Returns the contents of the currently active XML element. """
            return str(self.contentBuffer)
        
        def hasContents(self):
            """ Returns whether there is a non-empty content within the currently
             *  active XML element. """
            return bool(self.contentBuffer)
        
        def getParent(self):
            """ Returns the XML tag name of the parent of the currently active
                 *  XML element. """
            return self.tags.peek()
        
    """ The file extension for bzip2 files that is used for the automatic 
        detection of the file format. """
    BZ2_FILE_EXTENSION = ".bz2"

    def parseFile(self, dumpFile):  # throws WiktionaryException :
        """ Parses the given XML dump file. The file format is automatically
            detected using the file extension: it can be either bzip2 compressed
            or uncompressed XML. Internally, a SAX parser is used.
            @throws WiktionaryException in case of any parser errors. """
        try:
            self.parseStream(self.openDumpFile(dumpFile))
        except IOException as e:
            raise WiktionaryException(e)

    def parseStream(self, stream):  # throws IOException
        try:
            self.getParser().parse(stream, XMLDumpParser.XMLDumpHandler(self))
        except SAXException as e:
            raise WiktionaryException("XML parse error", e)
        finally:
            try:
                stream.close()
            except IOException:
                pass

    def onParserStart(self):
        """ Hotspot that is invoked on starting the parser. Use this hotspot to
            initialize your data. """

    def onElementStart(self, name, handler_):
        """ Hotspot that is invoked for each opening XML element. """

    def onElementEnd(self, name, handler_):
        """ Hotspot that is invoked for each closing XML element. """

    def onParserEnd(self):
        """ Hotspot that is invoked on finishing the parsing. Use this hotspot
            for cleaning up and closing resources. """

    @classmethod
    def openDumpFile(cls, dumpFile):  # throws IOException :
        # Open the dump file decompress if necessary.
        if dumpFile.getName().endswith(cls.BZ2_FILE_EXTENSION):
            return BZip2InputStream(dumpFile)
        else:
            return FileInputStream(dumpFile)

    def getParser(self):
        try:
            return self.getParserFactory()
        except ParserConfigurationException as e:
            raise WiktionaryException("SAX parser could not be configured", e)
        except SAXException as e:
            raise WiktionaryException("XML parse error", e)

    @classmethod
    def getParserFactory(cls):
        return xml.sax
